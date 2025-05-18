import requests
import json
import os
from dotenv import load_dotenv

print("Starting First Blood Notifier...")
# Load environment variables from .env file
load_dotenv()

# Configuration
CTFD_API_URL = os.getenv("CTFD_BASE_URL") + "/api/v1/submissions?type=correct"
NOTIFY_URL = os.getenv("SLACK_WEBHOOK_URL")
TOKEN = os.getenv("CTFD_TOKEN")
NOTIFIED_FILE = "/app/notified_challenges.json"

# Load already-notified challenges from file
if os.path.exists(NOTIFIED_FILE):
    with open(NOTIFIED_FILE, "r") as f:
        try:
            notified_challenges = json.load(f)
        except json.JSONDecodeError:
            notified_challenges = {}  # Reset if the file is corrupted
else:
    notified_challenges = {}

# Fetch correct submissions
headers = {
    "Authorization": "Bearer" + TOKEN,
    "Content-Type": "application/json"
}

response = requests.get(CTFD_API_URL, headers=headers)
if response.status_code != 200:
    print(f"Error fetching submissions: {response.status_code}, {response.text}")
    exit()

submissions = response.json().get("data", [])

# Create a dictionary to track the first solve for each challenge
first_bloods = {}

for submission in submissions:
    challenge_id = str(submission["challenge_id"])  # Ensure challenge_id is a string
    solve_date = submission["date"]

    # Skip if this challenge was already notified
    if challenge_id in notified_challenges:
        continue

    # Track the earliest solve for each challenge
    if challenge_id not in first_bloods or solve_date < first_bloods[challenge_id]["date"]:
        first_bloods[challenge_id] = {
            "date": solve_date,
            "user_name": submission["user"]["name"],
            "challenge_name": submission["challenge"]["name"]
        }

# Notify for each First Blood
for challenge_id, info in first_bloods.items():
    # Ensure we don't notify for challenges already in the notified list
    if challenge_id not in notified_challenges:
        # Notify the external service
        payload = {
            "text": f"First Blood on {info['challenge_name']} by {info['user_name']} :drop_of_blood:"
        }

        notify_response = requests.post(NOTIFY_URL, json=payload)
        if notify_response.status_code == 200:
            print(f"Notified for First Blood on challenge {challenge_id}")
            notified_challenges[challenge_id] = info["date"]  # Store challenge ID and date
        else:
            print(f"Failed to notify for challenge {challenge_id}: {notify_response.status_code}, {notify_response.text}")

# Save the notified challenges back to the file
with open(NOTIFIED_FILE, "w") as f:
    json.dump(notified_challenges, f, indent=4)

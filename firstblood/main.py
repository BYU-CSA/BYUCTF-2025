import requests
import json
import os
import re
from dotenv import load_dotenv

print("Starting First Blood Notifier...")

# Load environment variables from .env file
load_dotenv()

# Configuration
BASE_URL = os.getenv("CTFD_BASE_URL")
CTFD_API_URL = BASE_URL + "/api/v1/submissions?type=correct"
NOTIFY_URL = os.getenv("DISCORD_WEBHOOK_URL")
TOKEN = os.getenv("CTFD_TOKEN")
NOTIFIED_FILE = "/app/notified_challenges.json"

def sanitize_discord_content(text):
    return re.sub(r'([@&<>*_~`|])', r'\\\1', text)

# Load already-notified challenges from file
if os.path.exists(NOTIFIED_FILE):
    with open(NOTIFIED_FILE, "r") as f:
        try:
            notified_challenges = json.load(f)
        except json.JSONDecodeError:
            notified_challenges = {}
else:
    notified_challenges = {}

# Create a dictionary to track the first solve for each challenge
first_bloods = {}

# Fetch correct submissions with pagination
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

page = 1
per_page = 100  # Adjust if needed

while True:
    paged_url = f"{CTFD_API_URL}&page={page}&per_page={per_page}"
    response = requests.get(paged_url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching submissions (page {page}): {response.status_code}, {response.text}")
        break

    data = response.json().get("data", [])
    if not data:
        break  # No more pages

    for submission in data:
        challenge_id = str(submission["challenge_id"])
        solve_date = submission["date"]

        # Skip if this challenge was already notified
        if challenge_id in notified_challenges:
            continue

        # Track the earliest solve
        if challenge_id not in first_bloods or solve_date < first_bloods[challenge_id]["date"]:
            first_bloods[challenge_id] = {
                "date": solve_date,
                "user_name": submission["user"]["name"],
                "challenge_name": submission["challenge"]["name"]
            }

    page += 1

# Notify for each First Blood
for challenge_id, info in first_bloods.items():
    if challenge_id not in notified_challenges:
        info["user_name"] = sanitize_discord_content(info["user_name"])
        info["challenge_name"] = sanitize_discord_content(info["challenge_name"])

        payload = {
            "content": f"First Blood on {info['challenge_name']} by {info['user_name']} :drop_of_blood:"
        }

        try:
            notify_response = requests.post(NOTIFY_URL, json=payload)
            notify_response.raise_for_status()
            print(f"Notified for First Blood on challenge {challenge_id}")
            notified_challenges[challenge_id] = info["date"]
        except requests.exceptions.RequestException as e:
            print(f"Failed to notify for challenge {challenge_id}: {e}")

# Save the updated notified challenges
with open(NOTIFIED_FILE, "w") as f:
    json.dump(notified_challenges, f, indent=4)
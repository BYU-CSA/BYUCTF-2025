# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Copy the cron job file to the cron directory
COPY ctfd_cron /etc/cron.d/ctfd_cron

# Give execution rights on the cron job file
RUN chmod 0644 /etc/cron.d/ctfd_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Install cron
RUN apt-get update && apt-get install -y cron

# Run all scripts on container startup and start cron
CMD ["sh", "-c", "python /app/main.py && cron && tail -f /var/log/cron.log"]

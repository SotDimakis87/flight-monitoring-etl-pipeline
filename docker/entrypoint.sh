#!/bin/sh
set -e

# Export Docker environment variables so cron can access them
printenv > /etc/environment

# Ensure log directory exists
mkdir -p /app/data/logs

# Ensure log file exists
touch /app/data/logs/etl_cron.log

echo "Starting cron scheduler..."

# Start cron in the background
cron

echo "Cron scheduler started."
echo "ETL logs will be written to /app/data/logs/etl_cron.log"

# Keep container alive without tailing the Windows-mounted log file
while true; do
    sleep 60
done
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs appear immediately
ENV PYTHONUNBUFFERED=1

# Working directory inside the container
WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy dependency list first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ src/
COPY sql_scripts/ sql_scripts/
COPY docker/cron_job /etc/cron.d/etl_cron
COPY docker/entrypoint.sh /entrypoint.sh

# Prepare cron file and entrypoint
RUN sed -i 's/\r$//' /etc/cron.d/etl_cron /entrypoint.sh && \
    chmod 0644 /etc/cron.d/etl_cron && \
    crontab /etc/cron.d/etl_cron && \
    chmod +x /entrypoint.sh

# Start cron scheduler
CMD ["/entrypoint.sh"]
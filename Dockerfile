FROM python:3.12-slim

WORKDIR /app

# Install Chromium + chromedriver and runtime libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium chromium-driver \
    ca-certificates curl unzip \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 \
    libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libglib2.0-0 libgtk-3-0 \
    libnspr4 libnss3 libpango-1.0-0 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 \
    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 \
    libxss1 libxtst6 xdg-utils build-essential gcc g++ libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Project
COPY . .

# Runtime-only env (no secrets here)
# Use simplified config system with environment-specific properties
ENV ENVIRONMENT=dev \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

ENTRYPOINT ["pytest"]
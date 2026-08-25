# 1. Base OS Engine: Use an official, lightweight Python Linux image
FROM python:3.11-slim

# 2. System Level Packages: Install git in case your dependencies need it
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 3. Working Sandbox Directory: Establish our microservice root folder inside Linux
WORKDIR /app

# 4. System Tool Manifest: Copy your tool checklist into the Linux container
COPY requirements.txt .

# 5. Library Installation: Execute pip installation optimized for CPU environments
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --index-url https://pytorch.org

# 6. Copy Code Architecture: Copy all your python project folders into the container
COPY . .

# 7. Port Exposure: Open up the server communication highway on port 8000
EXPOSE 8000

# 8. Bootup Command: Launch Uvicorn server globally the millisecond the container starts
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

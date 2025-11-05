# Use Python base image
FROM python:3.11-slim

# Install curl for healthchecks and API calls
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose Flask port
EXPOSE 3000

# Default environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV OLLAMA_HOST=ollama
ENV OLLAMA_PORT=11434

# Command to run the application
CMD ["python", "app.py"]
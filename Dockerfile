FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000
EXPOSE 5000

# Remove ENV from Dockerfile - will be passed at runtime
CMD ["python", "main.py"]
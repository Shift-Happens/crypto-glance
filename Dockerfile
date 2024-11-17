FROM python:3.12.7-slim

# Set working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Expose port 5000
EXPOSE 5000

# Set the secret key as an environment variable to sign cookies
ENV FLASK_SECRET_KEY="FLASK_SECRET_KEY"

CMD ["python", "main.py"]
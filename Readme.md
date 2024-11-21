# Crypto Glance

A full-featured cryptocurrency monitoring application built with Flask that allows users to track Bitcoin addresses and set price alerts for various cryptocurrencies.
![image](https://github.com/user-attachments/assets/066e490d-d3e8-4575-be98-8cbbe5d8e484)

## Features

- 🔍 Bitcoin address lookup with balance and transaction history
- 💰 Real-time cryptocurrency price tracking (BTC, ETH, BNB, XRP, SOL)
- ⏰ Price alerts with email notifications 
- 📊 Transaction history visualization
- 📝 Search history management
- 📥 Export data to CSV format
- 🔗 Interactive transaction exploration

## Quick Start with Docker

Pull and run the official image:
```bash
docker run -d -p 5000:5000 \
  -e FLASK_SECRET_KEY="your-secret-key" \
  -e SMTP_SERVER="smtp.gmail.com" \
  -e SMTP_PORT="587" \
  -e SMTP_USERNAME="your-email@gmail.com" \
  -e SMTP_PASSWORD="your-password" \
  -e SMTP_SENDER="your-email@gmail.com" \
  shifthappens420/crypto-glance:latest
```

Docker Hub: [shifthappens420/crypto-glance](https://hub.docker.com/r/shifthappens420/crypto-glance)

### Build Locally

```bash
docker build -t crypto-glance .
docker run -d -p 5000:5000 -e FLASK_SECRET_KEY="your-secret-key" crypto-glance
```

### Standard Setup

1. Clone and install:
```bash
git clone https://github.com/your-username/crypto-glance.git
cd crypto-glance
pip install -r requirements.txt
```

2. Configure environment and run:
```bash
export FLASK_SECRET_KEY="your-secret-key"
python main.py
```

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for session management (required)
- `SMTP_SERVER`: SMTP server for email alerts
- `SMTP_PORT`: SMTP server port  
- `SMTP_USERNAME`: SMTP authentication username
- `SMTP_PASSWORD`: SMTP authentication password
- `SMTP_SENDER`: Email address for sending alerts
- `FLASK_ENV`: Set to `production` for deployment, `development` for local development

## Usage

1. Access the application at `http://localhost:5000`
2. Enter a Bitcoin address to view its balance and transactions
3. Monitor real-time cryptocurrency prices
4. Set price alerts with email notifications
5. Export address data or search history to CSV
6. Click on transaction addresses for quick lookup

## API Endpoints

- `GET /api/prices`: Get current cryptocurrency prices
- `POST /api/alerts`: Set price alert
- `DELETE /api/alerts`: Remove price alert 
- `POST /check_address`: Check Bitcoin address balance
- `POST /export_csv`: Export address data to CSV
- `POST /export_history`: Export search history to CSV

## Development

```bash
export FLASK_ENV=development
python main.py
```

## Production Deployment

The application includes Terraform configurations for AWS deployment using:
- ECS Fargate for container orchestration
- Application Load Balancer for traffic distribution
- VPC with public and private subnets
- CloudWatch for logging

Ensure to:
1. Configure AWS credentials
2. Set required variables in `terraform.tfvars`
3. Deploy using Terraform:
```bash
terraform init
terraform apply
```

## Built With

- Flask 3.1.0
- Requests 2.32.2
- Pandas 2.2.3
- Bootstrap 5.1.3
- Terraform

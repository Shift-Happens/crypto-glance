# Crypto Glance
![image](https://github.com/user-attachments/assets/4a991599-63ed-4965-897c-974bff4eb4f6)
A Bitcoin wallet explorer built with Flask that lets you check balances and transaction histories using the Blockchain.info API.

## Features


- 🔍 Look up any Bitcoin address balance
- 💰 View balance in both BTC and USD
- 📊 Display recent transactions with details
- 📝 Keep track of search history
- 📥 Export data to CSV format
- 🔗 Clickable transaction addresses for easy navigation

## Installation

### Standard Setup

1. Clone the repository:
```bash
git clone https://github.com/Shift-Happens/crypto-glance.git
cd crypto-glance
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t crypto-glance .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 -e FLASK_SECRET_KEY=your_secret_key crypto-glance
```

## Environment Variables

- `FLASK_SECRET_KEY`: Secret key for session management (required)
- `FLASK_ENV`: Set to `production` for deployment, `development` for local development

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Enter a Bitcoin address in the search box
3. View the current balance and USD equivalent
4. Check recent transactions in the transactions table
5. Click on addresses in transactions to look them up
6. Export data to CSV using the export buttons
7. Access your search history from the sidebar

## Development

For local development:
```bash
export FLASK_ENV=development
python main.py
```

## Production Deployment

Ensure to:
1. Set a secure `FLASK_SECRET_KEY`
2. Set `FLASK_ENV=production`
3. Use proper SSL/TLS termination
4. Configure appropriate rate limiting

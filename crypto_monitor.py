import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import time
from threading import Thread
import os

class CryptoMonitor:
    def __init__(self, smtp_config):
        self.alerts = {}  # {crypto_id: {user_email: {target_price: price, above: bool}}}
        self.smtp_config = smtp_config
        self.supported_cryptos = {
            'BTC': 'BTCUSDT',
            'ETH': 'ETHUSDT',
            'BNB': 'BNBUSDT',
            'XRP': 'XRPUSDT',
            'SOL': 'SOLUSDT'
        }
        
    def get_crypto_prices(self):
        """Get current prices from Binance API"""
        prices = {}
        try:
            # Use Binance API endpoint for 24hr ticker prices
            url = 'https://api.binance.com/api/v3/ticker/price'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Map response to our format
            for item in data:
                symbol = item['symbol']
                for crypto, pair in self.supported_cryptos.items():
                    if symbol == pair:
                        prices[crypto] = float(item['price'])
            
            return prices if prices else None
            
        except Exception as e:
            print(f"Error fetching prices from Binance: {str(e)}")
            return None

    def set_alert(self, crypto, email, target_price, above=True):
        """Set price alert for a cryptocurrency"""
        if crypto not in self.alerts:
            self.alerts[crypto] = {}
        if email not in self.alerts[crypto]:
            self.alerts[crypto][email] = {}
        
        self.alerts[crypto][email][target_price] = above
        return True

    def remove_alert(self, crypto, email, target_price):
        """Remove specific price alert"""
        if crypto in self.alerts and email in self.alerts[crypto]:
            self.alerts[crypto][email].pop(target_price, None)
            return True
        return False

    def send_email_alert(self, email, crypto, current_price, target_price, above):
        """Send email notification"""
        subject = f"Crypto Price Alert - {crypto}"
        body = f"""
        Price Alert for {crypto}!
        Current price: ${current_price}
        Target price: ${target_price}
        Condition: {'Above' if above else 'Below'}
        
        Check it out at: http://localhost:5000
        """
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.smtp_config['sender']
        msg['To'] = email
        
        try:
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['username'], self.smtp_config['password'])
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def check_alerts(self):
        """Check current prices against alerts"""
        prices = self.get_crypto_prices()
        if not prices:
            return
            
        for crypto, users in self.alerts.items():
            if crypto not in prices:
                continue
                
            current_price = prices[crypto]
            for email, alerts in users.items():
                for target_price, above in alerts.items():
                    if (above and current_price >= target_price) or \
                       (not above and current_price <= target_price):
                        self.send_email_alert(email, crypto, current_price, target_price, above)
                        self.remove_alert(crypto, email, target_price)

    def start_monitoring(self):
        """Start monitoring thread"""
        def monitor():
            while True:
                self.check_alerts()
                time.sleep(60)  # Check every minute
                
        thread = Thread(target=monitor, daemon=True)
        thread.start()
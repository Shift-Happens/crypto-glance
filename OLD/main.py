from flask import Flask, render_template, request, jsonify, send_file, session
import requests
import pandas as pd
from io import BytesIO
from datetime import datetime
from crypto_monitor import CryptoMonitor
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

def get_transactions(address):
    """Get transaction history for a Bitcoin address"""
    url = f"https://blockchain.info/rawaddr/{address}"
    btc_price_url = "https://blockchain.info/ticker"
    try:
        # Get BTC price in USD
        price_response = requests.get(btc_price_url)
        price_data = price_response.json()
        btc_usd_rate = price_data['USD']['last']

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        txs = data.get('txs', [])[:10]  # Get last 10 transactions
        
        return {
            'status': 'success',
            'data': [{
                'hash': tx['hash'],
                'time': datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M'),
                'amount': sum(out['value'] for out in tx['out']) / 100000000,
                'amount_usd': (sum(out['value'] for out in tx['out']) / 100000000) * btc_usd_rate,
                'from': [inp.get('prev_out', {}).get('addr', 'Unknown') for inp in tx.get('inputs', [])],
                'to': [out.get('addr', 'Unknown') for out in tx.get('out', [])]
            } for tx in txs]
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return {
                'status': 'error',
                'message': 'Rate limit exceeded. Please try again later.'
            }
        return {
            'status': 'error',
            'message': f'API error: {str(e)}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error fetching transactions: {str(e)}'
        }

def get_address_balance(address):
    """Get balance for a Bitcoin address using blockchain.info API"""
    url = f"https://blockchain.info/balance?active={address}"
    try:
        response = requests.get(url)
        data = response.json()
        balance_satoshi = data[address]['final_balance']
        balance_btc = balance_satoshi / 100000000
        transactions_result = get_transactions(address)
        return {
            "address": address,
            "balance": balance_btc,
            "transactions": transactions_result.get('data', []),
            "error": transactions_result.get('message') if transactions_result['status'] == 'error' else None
        }
    except Exception as e:
        return {
            "address": address, 
            "balance": 0, 
            "transactions": [], 
            "error": f"Failed to fetch balance: {str(e)}"
        }

@app.route('/')
def home():
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', history=session['history'])

@app.route('/check_address', methods=['POST'])
def check_address():
    address = request.form.get('address')
    result = get_address_balance(address)
    
    # Update history
    if 'history' not in session:
        session['history'] = []
    if address not in session['history']:
        session['history'].insert(0, address)
        session['history'] = session['history'][:10]  # Keep last 10
        session.modified = True
        
    return jsonify(result)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    address = request.form.get('address')
    result = get_address_balance(address)
    
    # Create DataFrame with transactions
    transactions_df = pd.DataFrame(result['transactions'])
    balance_df = pd.DataFrame([{
        'address': result['address'],
        'balance': result['balance']
    }])
    
    # Create CSV with multiple sections
    csv_buffer = BytesIO()
    balance_df.to_csv(csv_buffer, index=False)
    csv_buffer.write(b'\n\nTransactions:\n')
    transactions_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'bitcoin_balance_{address}.csv'
    )

@app.route('/export_history', methods=['POST'])
def export_history():
    if 'history' not in session:
        return jsonify({'error': 'No history found'})
    
    # Create DataFrame from history
    df = pd.DataFrame(session['history'], columns=['address'])
    
    # Create CSV buffer
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name='search_history.csv'
    )

# Initialize CryptoMonitor with configs
smtp_config = {
    'server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'port': int(os.getenv('SMTP_PORT', '587')),
    'username': os.getenv('SMTP_USERNAME', ''),
    'password': os.getenv('SMTP_PASSWORD', ''),
    'sender': os.getenv('SMTP_SENDER', '')
}

crypto_monitor = CryptoMonitor(smtp_config)
crypto_monitor.start_monitoring()

# Add new routes
@app.route('/api/prices', methods=['GET'])
def get_prices():
    try:
        prices = crypto_monitor.get_crypto_prices()
        if prices is None:
            return jsonify({'error': 'Failed to fetch prices'}), 500
        return jsonify(prices)
    except Exception as e:
        print(f"Error in get_prices route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/alerts', methods=['POST'])
def set_alert():
    data = request.json
    result = crypto_monitor.set_alert(
        data['crypto'],
        data['email'],
        float(data['target_price']),
        data.get('above', True)
    )
    return jsonify({'success': result})

@app.route('/api/alerts', methods=['DELETE'])
def remove_alert():
    data = request.json
    result = crypto_monitor.remove_alert(
        data['crypto'],
        data['email'],
        float(data['target_price'])
    )
    return jsonify({'success': result})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_file, session
import requests
import pandas as pd
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session

def get_transactions(address):
    """Get transaction history for a Bitcoin address"""
    url = f"https://blockchain.info/rawaddr/{address}"
    try:
        response = requests.get(url)
        data = response.json()
        txs = data.get('txs', [])[:10]  # Get last 10 transactions
        return [{
            'hash': tx['hash'],
            'time': datetime.fromtimestamp(tx['time']).strftime('%Y-%m-%d %H:%M'),
            'amount': sum(out['value'] for out in tx['out']) / 100000000
        } for tx in txs]
    except:
        return []

def get_address_balance(address):
    """Get balance for a Bitcoin address using blockchain.info API"""
    url = f"https://blockchain.info/balance?active={address}"
    try:
        response = requests.get(url)
        data = response.json()
        balance_satoshi = data[address]['final_balance']
        balance_btc = balance_satoshi / 100000000
        transactions = get_transactions(address)
        return {
            "address": address,
            "balance": balance_btc,
            "transactions": transactions
        }
    except:
        return {"address": address, "balance": 0, "transactions": [], "error": "Failed to fetch"}

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

if __name__ == '__main__':
    app.run(debug=True)
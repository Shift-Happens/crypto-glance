from flask import Flask, render_template, request, jsonify, send_file
import requests
import pandas as pd
from io import StringIO
import json

app = Flask(__name__)

def get_address_balance(address):
    """Get balance for a Bitcoin address using blockchain.info API"""
    url = f"https://blockchain.info/balance?active={address}"
    try:
        response = requests.get(url)
        data = response.json()
        balance_satoshi = data[address]['final_balance']
        balance_btc = balance_satoshi / 100000000  # Convert to BTC
        return {"address": address, "balance": balance_btc}
    except:
        return {"address": address, "balance": 0, "error": "Failed to fetch"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_address', methods=['POST'])
def check_address():
    address = request.form.get('address')
    result = get_address_balance(address)
    return jsonify(result)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    address = request.form.get('address')
    result = get_address_balance(address)
    
    df = pd.DataFrame([result])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    
    return send_file(
        StringIO(csv_buffer.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='bitcoin_balance.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
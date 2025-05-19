import json
import os
import time

import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, request

from api import API

debugger = True
CACHE_DIR = "Cached"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

app = Flask(__name__)

def fetch_all_data(symbol, interval='1m'):
    return API().fetchData(symbol=symbol, interval=interval)

@app.route('/fetch', methods=['GET'])
def fetch():
    try:
        symbol = request.args.get('symbol')
        interval = request.args.get('interval', '1m')

        if not symbol:
            return jsonify({"error": "Missing required parameter: symbol"}), 400

        data = fetch_all_data(symbol, interval)  # Should return a list of dicts
        return jsonify(data)  # Automatically converts list to JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/fetch_price', methods=['GET'])
def fetch_price():
    try:
        symbol = request.args.get('symbol')

        if not symbol:
            return jsonify({"error": "Missing required parameter: symbol"}), 400

        data = fetch_price(symbol)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if debugger:
    app.run(debug=False)

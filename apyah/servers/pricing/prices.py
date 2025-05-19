import json
import os
import time

import pandas as pd
import yfinance as yf
from flask import Flask, jsonify, request
from priceApi import PriceAPI

debugger = True
api = PriceAPI()

app = Flask(__name__)
    
@app.route('/price_ports', methods=['GET'])
def fetch_price():
    try:
        data = api.price_ports()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/toggle_port', methods=['POST'])
def toggle_port():
    try:
        data = request.get_json()
        port = data.get('port')
        status = data.get('status')

        if not port or status is None:
            return jsonify({"error": "Missing required parameters: port or status"}), 400

        api.toggle_port(port, status)
        return jsonify({"message": "Port toggled successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if debugger:
    app.run(debug=False, port=4997)

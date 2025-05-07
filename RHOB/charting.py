import os
import time
import json
import yfinance as yf
import pandas as pd
from flask import Flask, request, jsonify

debugger = True
CACHE_DIR = "Cached"

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

app = Flask(__name__)

class API:
    def __init__(self):
        pass

    def fetchData(self, symbol=None, period="1d"):
        if symbol is None:
            return None
        try:
            app.logger.debug(f"Fetching 1m data for symbol: {symbol}, period: {period}")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1m", prepost=True)
            data = data.reset_index()
            data['Datetime'] = data['Datetime'].apply(lambda x: x.isoformat())
            return {
                "interval": "1m",
                "records": data.to_dict(orient="records")
            }
        except Exception as e:
            app.logger.error(f"Error fetching data: {str(e)}")
            raise e
    


def get_cache_file_path(symbol):
    return os.path.join(CACHE_DIR, f"{symbol}.json")

def is_cache_valid(symbol):
    path = get_cache_file_path(symbol)
    if not os.path.exists(path): return False
    last_modified_minute = time.localtime(os.path.getmtime(path)).tm_min
    return last_modified_minute == time.localtime().tm_min

def save_cache(symbol, data):
    try:
        with open(get_cache_file_path(symbol), 'w') as f:
            json.dump(data, f)
        print("Saved")
    except Exception as e:
        app.logger.error(f"Error saving data to cache: {str(e)}")

def fetch_1m_data(symbol, period):
    return API().fetchData(symbol=symbol, period=period)

def aggregate_data(data, to_interval):
    df = pd.DataFrame(data)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df.set_index('Datetime', inplace=True)

    rule_map = {
        '5m': '5min', '15m': '15min', '30m': '30min', '1h': '1h'
    }

    if to_interval not in rule_map:
        raise ValueError("Unsupported interval")

    agg_df = df.resample(rule_map[to_interval]).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum'
    }).dropna()

    agg_df.reset_index(inplace=True)
    agg_df['Datetime'] = agg_df['Datetime'].apply(lambda x: x.isoformat())
    return agg_df.to_dict(orient="records")

@app.route('/fetch', methods=['GET'])
def fetch():
    symbol = request.args.get('symbol')
    period = request.args.get('period', '1d')
    interval = request.args.get('interval', '5m')

    if not symbol:
        return jsonify({"error": "Missing required parameter: symbol"}), 400

    try:
        if is_cache_valid(symbol):
            with open(get_cache_file_path(symbol), 'r') as f:
                try:
                    cached = json.load(f)
                    records = cached.get("records")
                    try:
                        if interval == "1m":
                            return jsonify(records)
                        converted = aggregate_data(records, interval)
                        return jsonify(converted)

                    except Exception as e:
                        app.logger.warning(f"Aggregation failed: {str(e)}")
                except Exception as e:
                    app.logger.error(f"Invalid cache format: {str(e)}")
                    os.remove(get_cache_file_path(symbol))

        else:
            try:
                fresh = fetch_1m_data(symbol, period)
                save_cache(symbol, fresh)
                        
                if interval == "1m":
                    return jsonify(fresh["records"])
                converted = aggregate_data(fresh["records"], interval)
                return jsonify(converted)
            except:
                with open(get_cache_file_path(symbol), 'r') as f:
                    try:
                        cached = json.load(f)
                        records = cached.get("records")
                        try:
                            if interval == "1m":
                                return jsonify(records)
                            converted = aggregate_data(records, interval)
                            return jsonify(converted)

                        except Exception as e:
                            app.logger.warning(f"Aggregation failed: {str(e)}")
                    except Exception as e:
                        app.logger.error(f"Invalid cache format: {str(e)}")
                        os.remove(get_cache_file_path(symbol))


    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

if debugger:
    app.run(debug=False)

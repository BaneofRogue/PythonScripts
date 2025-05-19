import json
import os
import time

import pandas as pd
from crawler import CrawlyTheGoat

from util import *

CACHE_DIR = "Cached"

class ChartAPI:
    def __init__(self):
        self.bot = CrawlyTheGoat(headless=True, debug_port=4999)

    def fetchData(self, symbol=None, interval='1m', startDate=None, endDate=None):
        if symbol is None:
            return None
        try:
            while True:
                if(self.is_cache_valid(symbol)):
                    with open(self.get_cache_file_path(symbol), 'r') as f:
                        data = json.load(f)
                        break # exit because we have data
                else:
                    print(f"Fetching 1m data for symbol: {symbol}")
                    data = self.bot.fetch_historical_data(symbol=symbol)
                    self.save_cache_data(symbol, data)
            try:
                data = self.aggregate_data(data, interval)
            except Exception as e:
                print(f"Error aggregating data: {e} returning 1m data")
            return data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            raise e
        
    def price_ports(self):
        try:
            data = self.bot.fetch_price_ports()
            return data
        except Exception as e:
            print(f"Error fetching price ports: {str(e)}")
            raise e
        
    def toggle_port(self, port, status):
        try:
            self.bot.toggle_port(port, status)
        except Exception as e:
            print(f"Error toggling port: {str(e)}")
            raise e
        
    def aggregate_data(self, data, to_interval):
        rule_map = {'1m': '1min','5m': '5min', '15m': '15min', '30m': '30min', '1h': '1h'}
        if to_interval not in rule_map:
            raise ValueError(f"Unsupported interval: {to_interval}")

        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp').resample(rule_map[to_interval]).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}).dropna().reset_index()

        df['timestamp'] = df['timestamp'].astype('int64') // 10**9
        return df.to_dict(orient='records')
    
    def get_cache_file_path(self, symbol):
        return os.path.join(CACHE_DIR, f"{symbol}.json")
    
    def is_cache_valid(self, symbol):
        path = self.get_cache_file_path(symbol)
        if not os.path.exists(path): return False
        last_modified_minute = time.localtime(os.path.getmtime(path)).tm_min
        return last_modified_minute == time.localtime().tm_min
    
    def save_cache_data(self, symbol, data):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        with open(self.get_cache_file_path(symbol), 'w') as f:
            json.dump(data, f)

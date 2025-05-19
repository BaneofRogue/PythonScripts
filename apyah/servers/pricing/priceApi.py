import json
import os
import time

import pandas as pd
from crawler import CrawlyTheGoat

CACHE_DIR = "Cached"

class PriceAPI:
    def __init__(self):
        self.bot = CrawlyTheGoat(headless=False, debug_port=4998)
        
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
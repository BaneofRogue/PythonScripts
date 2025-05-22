import json
import os
import time

from DrissionPage import ChromiumOptions, WebPage
from DrissionPage.common import Actions, By, Keys

from util import *

class CrawlyTheGoat:
    def __init__(self, tab_count=1, headless=False, profile_name=None, debug_port=None):
        self.options = ChromiumOptions()
        self.options.headless(headless)
        self.options.mute(True)
        
        # Set download path specific to the profile
        ############################################################
        if(profile_name != None):
            download_path = os.path.join(os.getcwd(), 'downloads', profile_name)
            os.makedirs(download_path, exist_ok=True)
            self.options.set_download_path(download_path)
        ############################################################
        # Set Chrome user profile and local debugging port
        ############################################################
        if(profile_name != None or debug_port != None):
            self.options.set_user(profile_name)
            self.options.set_local_port(debug_port)
        ############################################################

        # Initialize the WebPage with the configured options
        self.page = WebPage(chromium_options=self.options)
        self.tabs = []
        self.actions = []

        self.table = None
        self.indexes = []
        
        # Set up tabs and actions
        self.better_actions_setup(tab_count)
        
    def check_tab_count(self):
        tab_count = 0
        while True:
            try:
                self.page.get_tab(id_or_num=tab_count+1)
                tab_count += 1
            except Exception as e:
                break
            
        return tab_count
    
    def better_actions_setup(self, num_tabs):
        tab_count = self.check_tab_count()
        if(tab_count > num_tabs):
            print("Tab count mismatch. Expected:", num_tabs, "but got:", self.check_tab_count())
            print("Ignoring extra tabs.")
        else:
            print("Tab count mismatch. Expected:", num_tabs, "but got:", self.check_tab_count())
            print("Creating new tabs.")
            for item in range(tab_count, num_tabs):
                print("Creating new tab:", item)
                self.page.new_tab()
        
        for item in range(1, num_tabs+1):
            new_tab = self.page.get_tab(id_or_num=item)
            self.tabs.append(new_tab)
            self.actions.append(Actions(new_tab))
            print(f"Setup tab: {item} out of {num_tabs}")
            
        time.sleep(1)
            
    def is_valid_json(self, data):
        try:
            json_string = json.dumps(data)     # Serialize to JSON
            json.loads(json_string)           # Parse back to ensure it's valid JSON
            return True
        except (TypeError, ValueError):
            return False
          
    def name_to_index(self, name):
        if name in self.indexes:
            return self.indexes.index(name)
        else:
            print(f"Index '{name}' not found.")
            return None
        
    def index_to_symbol(self, index):
        return self.table[index].children()[1].text
        
    def name_to_data(self, name, i):
        index = self.name_to_index(name)
        if(index is not None):
            return self.table[i].children()[index].text
        else:
            return ""

    def fetch_prices(self):
        table = self.table
        all_prices = {}

        for i in range(20):
            if i >= len(table):
                break
            
            last_price = self.name_to_data("Last Price", i)

            after_text = self.name_to_data("After Hours", i).strip()
            after_price = after_text[1:] if after_text else ""
            after_percentage = after_text[0] if after_text else ""

            overnight_text = self.name_to_data("Overnight", i).strip()
            overnight_price = overnight_text[1:] if overnight_text else ""
            overnight_percentage = overnight_text[0] if overnight_text else ""

            all_prices[f"{self.index_to_symbol(i)}"] = {
                "market": last_price,
                "after_market": f"{after_percentage}{after_price}",
                "overnight": f"{overnight_percentage}{overnight_price}",
                "volume": self.name_to_data("Volume", i),
                "avg_volume": self.name_to_data("Avg Vol (3M)", i),
                "market_cap": self.name_to_data("Market Cap", i),
                "per_change": self.name_to_data("% Change", i),
            }
            
        return all_prices

    def find_ele(self, tab, target_text):
        current = tab.ele("#app").children().filter_one.text(target_text)
        if not current:
            print("Initial match not found.")
            return None

        while True:
            if current.text == target_text:
                return current

            next_elem = current.children().filter_one.text(target_text)
            if next_elem:
                current = next_elem
            else:
                return None

    def fetch_historical_data(self, symbol, prepost=True, startDate=None, endDate=None):    
        
        if(startDate == None and endDate == None):
            startDate = int(time.time()) - (6 * 24 * 60 * 60)
            endDate = int(time.time() + (60 * 20)) # + 20 minutes
        
        target = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?period1={startDate}&period2={endDate}&interval=1m&includePrePost={prepost}&events=div%7Csplit%7Cearn&lang=en-US&region=US&source=cosaic"
        
        tab = self.tabs[0]
        
        while True:
            tab.get(target)
            
            data = tab.s_ele('@tag()=pre').raw_text
            
            # check if data is proper json:
            if(self.is_valid_json(data)):
                print("Data is valid JSON")
                break
            else:
                print("Data is not valid JSON")
                print("Retrying in 1 second...")
                time.sleep(1)
                
        # parse the data
        print("Parsing data...")
        parser = Parser(symbol, json.loads(data), 'yahoo')
        
        candles = parser.generate_candles()
        
        return candles

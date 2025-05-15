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

        # Set up tabs and actions
        self.action_setup(tab_count)

    def action_setup(self, num_tabs):
        first = self.page.get_tab()
        self.tabs.append(first)
        self.actions.append(Actions(first))

        for _ in range(1, num_tabs):
            new_tab = self.page.new_tab()
            self.tabs.append(new_tab)
            self.actions.append(Actions(new_tab))
            
    def is_valid_json(self, data):
        try:
            json_string = json.dumps(data)     # Serialize to JSON
            json.loads(json_string)           # Parse back to ensure it's valid JSON
            return True
        except (TypeError, ValueError):
            return False

    def fetch_historical_data(self, symbol, prepost=True, startDate=None, endDate=None):
        
        if(startDate == None and endDate == None):
            startDate = int(time.time()) - (6 * 24 * 60 * 60)
            endDate = int(time.time())
        
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

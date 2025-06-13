import json
import os
import time
from datetime import datetime

from crawler import CrawlyTheGoat


class Zillo:
    
    def __init__(self, tab_count=1, headless=False, profile_name=None, debug_port=None):
        self.crawler = CrawlyTheGoat(tab_count=tab_count, headless=headless, profile_name=profile_name, debug_port=debug_port)
        self.tabs = self.crawler.tabs
        self.actions = self.crawler.actions
        self.crawler.debug = True
        self.setup_zillo()
        
    def setup_zillo(self):
        target_url = "https://www.zillow.com/"
        self.crawler.go_to(target_url, tab_id=0, force=False)
        
    def search_zillo(self, search_term):
        tab = self.tabs[0]
        actions = self.actions[0]
        url = tab.url
        if "zillow.com/" not in url:
            print("Not on Zillow page.")
            self.crawler.go_to("https://www.zillow.com/", tab_id=0, force=True)
        else:
            if url == "https://www.zillow.com/":
                main = tab.ele(".znav-transparent").child().children()[1].child().child().child().children()[1].child().child().child().child().child().child().child()
                search_box = main.child()
                search_box.click()
                print("Clicked on search box")
                actions.type(search_term)
                actions.wait(3)
                search_list = main.parent().children()[1].child().children()
                for item in search_list:
                    text = item.children()[1].raw_text.strip()
                    print(f"Item text: {text}")
                    if text == search_term:
                        item.click()
                        return True
            else:
                pass
            
    def process(self, search_term):
        result = self.search_zillo(search_term)
        while result is False:
            print("failed search...")
            time.sleep(10)
        self.crawler.listen(0, packet_count=500, method=("PUT"), res_type="Fetch")
    
        
z = Zillo()
#z.process("Manhattan, New York, NY")

input("Press Enter to continue...")
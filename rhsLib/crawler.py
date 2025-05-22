import json
import os
import random
import time

from DrissionPage import ChromiumOptions, WebPage
from DrissionPage.common import Actions, By, Keys
import threading

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
        
    def do_loop(self):
        tab = self.tabs[0]
        
        while True:
            tab.set.cookies.clear()
            tab.get("https://rockvillerampage.com/")
            
            print("searching for poll...")
            time.sleep(2)
            items = tab.ele(".poll-answers-container").children()
            
            radio = items[6]
            
            radio = radio.child().child()
            radio.click()
            print(radio.states.is_selected)
            print("Clicked on the last item.")
            
            button = items[7]
            print("Button found:", button)
            button.click()
            print("Vote button clicked.")
            
            tab.set.cookies.clear()
            print("Cookies cleared.")
            print("Waiting for 5 seconds before next iteration.")
            time.sleep(5)
        
def run_crawler_on_port(port):
    try:
        c = CrawlyTheGoat(debug_port=port, headless=random.choice([True, True, True, True, True, True, True, False]))
        c.do_loop()
        print(f"Port {port} is available.")
    except Exception as e:
        print(f"Port {port} is already in use. Trying next port.")

threads = []
for port in range(9222, 9242):
    t = threading.Thread(target=run_crawler_on_port, args=(port,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
    
input()
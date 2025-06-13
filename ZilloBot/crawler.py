import json
import os
import time

from DrissionPage import ChromiumOptions, WebPage
from DrissionPage.common import Actions, By, Keys


class CrawlyTheGoat:
    def __init__(self, tab_count=1, headless=False, profile_name=None, debug_port=None):
        self.options = ChromiumOptions()
        self.options.headless(headless)
        self.options.mute(True)
        
        self.debug = False
        
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
        self.price_ports = {}
        self.set_price_ports = False
        
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
            
    def go_to(self, url=None, tab_id=None, force=False):
        if(url == None):
            raise ValueError("URL cannot be None")
        if(tab_id == None):
            raise ValueError("Tab ID cannot be None")
        if(tab_id > (len(self.tabs)-1)):
            raise ValueError("Tab ID exceeds the number of tabs")
        tab = self.tabs[tab_id]
        
        if(force == True):
            self.log("Force loading URL: " + url)
            tab.get(url)
        else:
            while(tab.url_available == False):
                self.log("Waiting for url to load...")
                time.sleep(0.1) # just keep waiting
                
            # after loaded, check if the URL is the same
            if(tab.url != url):
                self.log("URL mismatch. Expected: " + url + " but got: " + tab.url)
                self.log("Loading URL: " + url)
                tab.get(url)
                
    def listen(self, tab_id=None, packet_count=500, res_type=None, method=None):
        if tab_id is None:
            raise ValueError("Tab ID cannot be None")
        if tab_id >= len(self.tabs):
            raise ValueError("Tab ID exceeds the number of tabs")

        tab = self.tabs[tab_id]
        tab.listen.start(method=method, res_type=res_type)
        self.log(f"Listening on tab {tab_id} for packets...")

        collected = []
        i = 0

        try:
            for packet in tab.listen.steps(timeout=15):
                print(f"\n📦 URL: {packet.url}")
                print(f"Method: {packet.method}")
                print(f"Resource Type: {packet.resourceType}")

                try:
                    data = packet.response.body
                    packet_data = {
                        "url": packet.url,
                        "method": packet.method,
                        "resourceType": packet.resourceType,
                        "status": packet.response.status,
                        "body": data if isinstance(data, dict) else str(data)
                    }
                    collected.append(packet_data)

                    if isinstance(data, dict):
                        print("📊 Data:")
                        print(json.dumps(data, indent=2))
                    else:
                        print("📄 Raw response:")
                        print(data)
                except Exception as e:
                    print(f"❌ Error reading response: {e}")

                i += 1
                if i >= packet_count:
                    break

        except Exception as e:
            print(f"❌ Listener error: {e}")

        output_file = f"packets_{tab_id}.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(collected, f, indent=2, ensure_ascii=False)
            print(f"\n✅ Saved {len(collected)} packets to {output_file}")
        except Exception as e:
            print(f"❌ Failed to save packets: {e}")
                
    def log(self, message):
        if(self.debug == True):
            print(message)
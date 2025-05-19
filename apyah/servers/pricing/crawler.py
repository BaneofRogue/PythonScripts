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
            
        time.sleep(1)
        self.setup_screener()
        
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

    def setup_screener(self):
        tab = self.tabs[0]
        target = "https://app.webull.com/screener"
        
        if not (tab.url == target):
            print(f"{tab.url} is not {target}")
            tab.get(target)

        #tab.ele("text=My Screeners").click()

        #if len(tab.eles("text=>=100B")) != 2:
        time.sleep(0.5)
        tab.ele("#tabs_lv2_2").click()
        time.sleep(0.5)

        buttons = tab.eles(".simplebar-content-wrapper")[0].child().child().children()

        buttons[1].click()
        time.sleep(1)
        buttons[0].click()

        time.sleep(1)
        tbody = tab.ele("@tag()=tbody")
        self.table = tbody.children()
        index_es = tab.ele("@tag()=thead").child().children()
        
        for index in index_es:
            self.indexes.append(index.raw_text)
            
        print(f"Table setup complete: {self.indexes}")

        self.table.pop(0)
        self.table.pop(-1)
            
    def fetch_price_ports(self):
        if(self.set_price_ports):
            print("Price ports already set.")
            return self.price_ports
        
        if(self.table == None):
            return {}
        
        # {symbol, port, 5001++}
        self.set_price_ports = True
        port = 5001
        selectors = []
        keys = self.indexes
        ports = []
        
        for item in self.table:
            symbol = item.children()[1].text
            port += 1
            
            selectors.append(item.css_path)
            ports.append({"port": port, "enabled": True})
            
            self.price_ports[symbol] = port
            
        print(f"Price ports: {self.price_ports}")
        
        self.tabs[0].run_js_loaded(
        f"""
            const keys = {keys};
            const selectors = {selectors};
            const ports = {json.dumps(ports)};

            const sockets = []

            function createPersistentSocket(selector, port, index) {{
            const ws = new WebSocket("ws://127.0.0.1:" + port);
            sockets[index] = ws;

            ws.onopen = () => {{
                ws.send("yes");
                sendStructuredData(selector, ws);
            }};

            ws.onclose = () => {{
                // Try reconnecting after 1 second
                setTimeout(() => createPersistentSocket(selector, port, index), 1000);
            }};

            ws.onerror = (err) => {{
                console.error("WebSocket error:", err);
                ws.close();
            }};

            ws.onmessage = (event) => {{
                // handle incoming messages if needed
            }};
            }}

            function sendStructuredData(selector, ws) {{
            const parent = document.querySelector(selector);
            if (!parent) {{
                console.error("Parent selector not found:", selector);
                return;
            }}

            const children = parent.children;
            const data = {{}};

            for (let i = 0; i < keys.length; i++) {{
                data[keys[i]] = i < children.length ? children[i].textContent : null;
            }}

            if (ws.readyState === WebSocket.OPEN) {{
                ws.send(JSON.stringify(data));
            }}
            }}

            // Send data every second on all open sockets
            setInterval(() => {{
            for (let i = 0; i < selectors.length; i++) {{
                const portObj = ports[i];
                const ws = sockets[i];
                if (selectors[i] && portObj && portObj.enabled && ws && ws.readyState === WebSocket.OPEN) {{
                sendStructuredData(selectors[i], ws);
                }}
            }}
            }}, 1000);

            // Initial connections
            for (let i = 0; i < selectors.length; i++) {{
            const portObj = ports[i];
            if (selectors[i] && portObj && portObj.enabled) {{
                createPersistentSocket(selectors[i], portObj.port, i);
            }}
        }}
        """
        )

        return self.price_ports
    
    def toggle_port(self, port, value):
        self.tabs[0].run_js_loaded(
            f"""
            const portObj = ports.find(p => p.port === {port});
            if (portObj) {{
                portObj.enabled = {json.dumps(value)};
            }}
            """
        )
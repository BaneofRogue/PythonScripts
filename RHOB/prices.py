from flask import Flask, jsonify
from crawler import CrawlyTheGoat
import time
from datetime import datetime
import threading
import os

app = Flask(__name__)

class DataGrabber:

    def __init__(self):
        self.bot = CrawlyTheGoat(headless=True)
        self.tabs = self.bot.tabs
        self.table = None
        print("Setting up screener")
        self.setup_screener()
        print("Setting up screener DONE")

    def setup_screener(self):
        tab = self.tabs[0]
        target = "https://app.webull.com/screener"
        
        if not (tab.url == target):
            print(f"{tab.url} is not {target}")
            tab.get(target)

        tab.ele("text=My Screeners").click()

        if len(tab.eles("text=>=100B")) != 2:
            print("This is new!")
            tab.ele("#tabs_lv2_2").click()

            buttons = self.find_ele(tab, "High market value US stocks").parent().parent().parent().children()

            buttons[1].click()
            time.sleep(1)
            buttons[0].click()

            label = self.find_ele(tab, "Quote")
            lab = tab.eles(f".{label.attrs.get('class')}")[1].parent().children()[1].child().child().children()[1].text
        
            labs = tab.eles(f"text={lab}")
            self.table = labs[0].parent().parent().parent().parent().children()

            self.table.pop(0)
            self.table.pop(-1)

    def get_all_prices(self):
        table = self.table
        all_prices = {}

        for i in range(20):
            items = table[i].children()
            symbol = items[1].text
            last_price = items[3].text
            after_text = items[4].text.strip()
            overnight_text = items[11].text.strip()

            after_percentage = after_text[0]  # "+" or "-"
            after_price = after_text[1:]

            overnight_percentage = overnight_text[0]
            overnight_price = overnight_text[1:]

            all_prices[symbol] = {
                "market": last_price,
                "after_market": f"{after_percentage}{after_price}",
                "overnight": f"{overnight_percentage}{overnight_price}"
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

    def get_price(self, symbol):
        all_prices = self.get_all_prices()
        return all_prices.get(symbol, None)

data_grabber = DataGrabber()

@app.route('/fetchPrices', methods=['GET'])
def fetch_prices():
    prices = data_grabber.get_all_prices()
    return jsonify(prices)


if __name__ == "__main__":
    app.run(port=4999)

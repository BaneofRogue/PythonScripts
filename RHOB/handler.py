from crawler import CrawlyTheGoat
import time
from datetime import datetime
from collections import defaultdict
import os

class OrderBook:

    def __init__(self):
        self.bot = CrawlyTheGoat()
        self.tab = self.bot.tabs[0]

        self.target = "https://robinhood.com/stocks/8f92e76f-1e0e-4478-8580-16a6ffcfaef5/chart"

        self.logger = Log(debug=False)

        self.order_thresh = int(input("An order must have more than: (int) "))
        self.exclude_after = float(input("Exclude when price differs XXX from the current price: (float) "))

        self.setup()
        time.sleep(2)

        self.looper()

    def log(self, message, debug):
        self.logger.printer(message, debug)

    def setup(self):

        if(self.tab.url != self.target):
            self.tab.get(self.target)

    def getOrderBook(self):
        self.log("Called orderbook", True)
        app = self.tab.ele(".app")
        app_child = app.children()[1]
        book = app_child.child().child().children()[1].child().child().children()[1].child().children()[2].child().child()
        book2 = book.parent().children()[2].children()
        orders = book.children()
        orders.extend(book2)
        cleaned = []

        current_price = self.getPrice()

        for item in orders:
            price = float(item.children()[2].text.strip().replace(",", "").replace("$", ""))
            if(abs(price - current_price) > self.exclude_after):
                pass
            else:
                amount = int(item.children()[1].text)
                if(amount > self.order_thresh):
                    order_type = "buy"
                    if(price > current_price):
                        order_type = "sell"
                    cleaned.append(Order(price, amount, order_type))

        self.log("Got orderbook", True)

        for item in cleaned:
            self.log(f"{item.order_type.upper()} Order for: {item.amount} shares at {item.price}", debug=True)

        self.extract_key_levels(cleaned, depth=10, wallsize=500)

    def getPrice(self):
        self.log("Getting price", True)
        app = self.tab.ele(".app")
        app_child = app.children()[1]
        price_tag = app_child.child().child().child().child().children()[2].child()
        self.log("Got price", True)
        return float(price_tag.text.strip().replace(",", "").replace("$", ""))

    def extract_key_levels(self, orders, depth=10, wallsize=500, price_merge_range=0.10):
        os.system('cls')
        self.log("\nEXTRACTING KEY LEVELS (MERGED)", False)
        grouped = {"buy": [], "sell": []}

        for order in orders:
            grouped[order.order_type].append((order.price, order.amount))

        results = []

        buy_walls = []
        sell_walls = []


        for side in ["buy", "sell"]:
            grouped[side].sort(reverse=(side == "buy"))  # Still needed for proper merging behavior

            merged = []

            for price, amount in grouped[side]:
                found = False
                for entry in merged:
                    min_p, max_p, total = entry
                    if min_p - price_merge_range <= price <= max_p + price_merge_range:
                        entry[0] = min(min_p, price)
                        entry[1] = max(max_p, price)
                        entry[2] += amount
                        found = True
                        break
                if not found:
                    merged.append([price, price, amount])

            walls = [(pmin, pmax, amt) for pmin, pmax, amt in merged if amt >= wallsize]

            # Sort by minimum price ascending for both buy and sell
            walls.sort(key=lambda x: x[0])

            for pmin, pmax, total in walls[:depth]:
                if abs(pmax - pmin) < 0.01:
                    price_str = f"${pmin:.2f}"
                else:
                    price_str = f"${pmin:.2f} - ${pmax:.2f}"

                side_color = OrderColors.BUY if side == "buy" else OrderColors.SELL

                self.log(f"LEVEL: {side_color}{side.upper()}{OrderColors.RESET} wall at {price_str} with {total} shares", False)

            buy_strength = sum(amt for _, _, amt in buy_walls)
            sell_strength = sum(amt for _, _, amt in sell_walls)

        def wall_score(walls):
            return sum(amt ** 1.2 for _, _, amt in walls)  # amplify big walls

        buy_strength = wall_score(buy_walls)
        sell_strength = wall_score(sell_walls)


        if buy_strength > sell_strength:
            self.log("STRONGER SIDE: BUY", False)
        elif sell_strength > buy_strength:
            self.log("STRONGER SIDE: SELL", False)
        else:
            self.log("STRONGER SIDE: NEUTRAL", False)

    def looper(self):
        while True:
            try:
                self.getOrderBook()
                time.sleep(0.5)
            except Exception as e:
                print(e)

class Order:

    def __init__(self, price, amount, order_type):
        self.price = price
        self.amount = amount
        self.order_type = order_type

class OrderColors:
    SELL = '\033[91m'
    BUY = '\033[92m'
    RESET = '\033[0m'

class Log:

    def __init__(self, debug):
        self.debug = debug

    def printer(self, message, debug):
        if(self.debug == True):
            print(f"DEBUG || {datetime.now().isoformat()} || {message}")

        elif(debug == False):
            print(message)

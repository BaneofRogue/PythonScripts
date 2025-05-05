from crawler import CrawlyTheGoat

class DataGrabber:

    def __init__(self):

        self.bot = CrawlyTheGoat(headless=False)

        self.tabs = self.bot.tabs

        self.previous_price = 0
        self.current_price = 0

        time.sleep(5)

        self.looper()

    def get_id_from_symbol(self, symbol):
        symbol_to_id = {
            "SPY": 913243251,
            "AAPL": 913256135,
            "GOOG": 913303964,
            "NVDA": 913257561,
            "QQQ": 913243249,
            "TSLA": 913255598,
            "PLTR": 950172475
        }
        return symbol_to_id.get(symbol, None)  # Returns None if the symbol isn't found


    def get_price(self, symbol):
        # Return the price of SPY
        symbol_id = self.get_id_from_symbol(symbol)
        target = f"https://app.webull.com/stocks?action=stock_recntly&tickerId={symbol_id}"
        if(!(self.tabs[0].url == target)):
            self.tabs[1].get(target)
        
        tab = self.tabs[0]
        market_price_class = ".price  g-clickable"

        market_open_price = tab.ele(market_price_class)

        try:
            if datetime.now().hour >= 9 and datetime.now().hour <= 16:
                price = float(market_open_price.text.strip())
            else:
                price = float(market_open_price.parent().parent().parent().children()[2].children()[1].child().text.strip().replace(":", ""))
        except ValueError:
            return self.current_price  # Avoid breaking execution if conversion fails

        if price != self.current_price:
            now = datetime.now()
            print(f"{now.hour}:{now.minute}:{now.second}: {price}")

        self.previous_price, self.current_price = self.current_price, price

        return self.current_price

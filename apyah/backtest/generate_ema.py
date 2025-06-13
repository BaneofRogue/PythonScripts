import json
import os


class GenerateEMA:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.current_dir, f"{symbol}_formatted.json")
        self.load()
    
    def load(self):
        with open(self.json_path, "r") as f:
            self.data = json.load(f)
        
        if isinstance(self.data, str):
            try:
                self.data = json.loads(self.data)
            except json.JSONDecodeError:
                raise ValueError("Data is not valid JSON.")
            
    def generate_candles(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        # heres the candle data format:
        """
        [
            {
                "timestamp": 1590499800,
                "open": 301.92999267578125,
                "high": 302.19000244140625,
                "low": 295.4599914550781,
                "close": 299.0799865722656
            },
            {
                "timestamp": 1590586200,
                "open": 302.1199951171875,
                "high": 303.57000732421875,
                "low": 296.8699951171875,
                "close": 303.5299987792969
            },
        """
        # after "close", you should inject "ema{length}": value
        # generate an EMA value. The current data is 1 day per candle. Generate 21, 50, 100, 200 EMA for each candle.
        
        ema_lengths = [21, 50, 100, 200]
        closes = [candle["close"] for candle in self.data]
        emas = {length: [] for length in ema_lengths}

        def calc_ema(prices, length):
            ema = []
            k = 2 / (length + 1)
            for i, price in enumerate(prices):
                if i == 0:
                    ema.append(price)
                else:
                    ema.append(price * k + ema[-1] * (1 - k))
            return ema

        for length in ema_lengths:
            emas[length] = calc_ema(closes, length)

        for idx, candle in enumerate(self.data):
            for length in ema_lengths:
                candle[f"ema{length}"] = emas[length][idx]

        return self.data
    
ge = GenerateEMA("SPY")

the_data = ge.generate_candles()

# save to spy_ema.json
with open("spy_ema.json", "w") as f:
    json.dump(the_data, f, indent=4)
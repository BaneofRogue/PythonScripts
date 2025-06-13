import json
import os


class Parser:
    def __init__(self):
        
        # read from SPY.json and load the data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        spy_json_path = os.path.join(current_dir, "SPY.json")
        with open(spy_json_path, "r") as f:
            self.data = json.load(f)
        self.data = self.data.get('chart', {}).get('result', [{}])[0]
        
        if isinstance(self.data, str):
            try:
                self.data = json.loads(self.data)
                print("YAYYYYYYYYY")
            except json.JSONDecodeError:
                raise ValueError("Data is not valid JSON.")
        else:
            print("yall is good")
            # print available getters
            print("here are the available getters:")
            print(self.data.keys())
    
    def get_meta(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        return self.data.get('meta', {})
    
    def get_current_period_stamps(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        return self.get_meta().get('currentTradingPeriod', [])
    
    def valid_ranges(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        return self.get_meta().get('validRanges', [])
    
    def get_timestamps(self, index=None):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        if index is None:
            return self.data.get('timestamp', [])
        
        return self.data.get('timestamp', [])[index]
    
    def get_indices(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        indicators = self.data.get('indicators', {})  # Default to dict, not list
        quote_list = indicators.get("quote", [])
        return quote_list[0] if quote_list else {}

    def get_close(self, index):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        if( index < 0 or index >= len(self.get_timestamps())):
            raise IndexError("Index out of range.")
        
        return self.get_indices().get('close', [])[index]
    
    def get_open(self, index):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        timestamps = self.get_timestamps()
        if index < 0 or index >= len(timestamps):
            raise IndexError("Index out of range.")
        
        indices = self.get_indices()  # Should be a dict
        open_list = indices.get('open', [])  # get the list of open values
        if index >= len(open_list):
            raise IndexError("Index out of range in 'open' data.")
        
        return open_list[index]
   
    def get_high(self, index):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        if( index < 0 or index >= len(self.get_timestamps())):
            raise IndexError("Index out of range.")
        
        return self.get_indices().get('high', [])[index]
    
    def get_low(self, index):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        if( index < 0 or index >= len(self.get_timestamps())):
            raise IndexError("Index out of range.")
        
        return self.get_indices().get('low', [])[index]
    
    def generate_candle(self, index):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        if index < 0 or index >= len(self.get_timestamps()):
            raise IndexError("Index out of range.")
        
        return {
            'timestamp': self.get_timestamps(index),
            'open': self.get_open(index),
            'high': self.get_high(index),
            'low': self.get_low(index),
            'close': self.get_close(index)
        }
        
    def generate_candles(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        return [self.generate_candle(i) for i in range(len(self.get_timestamps()))]
    
# save data to json

p = Parser()

the_data = p.generate_candles()

with open("candles.json", "w") as f:
    json.dump(the_data, f, indent=4)
    print("Data saved to candles.json")
import json
import os


class Cleaner:
    
    def __init__(self, symbol, passed_data, data_type):
        self.file_path = os.path.join(os.getcwd(), 'Cached', f"{symbol}.json")
        self.data_type = data_type
        self.data = passed_data
            
    def organize(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        if self.data_type == 'yahoo':
            return self.data
                
        elif self.data_type == 'investing':
            return self._organize_investing_data()
            
        else:
            raise ValueError("Unsupported data type. Use 'yahoo' or 'investing'.")
        
    def _organize_investing_data(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load() method first.")
        
        # assume the data is in this format:
        """
        {
            "t": [
                1746816309,
                1746816369,
                1746816429,
                1746816489,
                1746816549
            ],
            "c": [
                
            ],
            "o": [
                
            ],
            "h": [
                
            ],
            "l": [
                
            ],
            "v": [
                
            ],
            "vo": [
                
            ],
            "vac": [
                
            ],
            "s": "ok",
        }
        """

        # we want to convert the data into this format:
        """
        {
            "chart": {
                "result": [
                    {
                        "meta": {
                            
                        },
                        "timestamp": [
                            1746816309,
                            1746816369,
                            1746816429,
                            1746816489,
                            1746816549
                        ],
                        "indicators": {
                            "quote": [{
                                "open": [],
                                "high": [],
                                "low": [],
                                "close": [],
                                "volume": []
                            }]
                        }
                    }
                ]
            }
        }
        """
        
        organized_data = {
            "chart": {
                "result": [
                    {
                        "meta": {},
                        "timestamp": self.data.get('t', []),
                        "indicators": {
                            "quote": [{
                                "open": self.data.get('o', []),
                                "high": self.data.get('h', []),
                                "low": self.data.get('l', []),
                                "close": self.data.get('c', []),
                                "volume": self.data.get('v', [])
                            }]
                        }
                    }
                ]
            }
        }
        
        return json.dumps(organized_data)

class Parser:
    def __init__(self, symbol, passed_data, data_type):
        self.data = Cleaner(symbol, passed_data, data_type).organize()
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
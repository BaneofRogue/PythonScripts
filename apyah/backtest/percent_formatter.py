import json
import os

data = []

path = os.path.join('backtest', 'SPY_formatted.json')
with open(path, 'r') as file:
    data = json.load(file)

def convert_to_percent_change(data):
    result = []
    
    candle_number = 0

    for i, candle in enumerate(data):
        if i == 0:
            base = candle['open']  # First candle based on its own open
        else:
            base = data[i-1]['close']  # Subsequent candles based on previous close

        percent_change_candle = {
            "timestamp": candle_number,
            "open": round((candle["open"] - base) / base * 100, 2),
            "high": round((candle["high"] - base) / base * 100, 2),
            "low": round((candle["low"] - base) / base * 100, 2),
            "close": round((candle["close"] - base) / base * 100, 2)
        }
        result.append(percent_change_candle)
        candle_number += 1

    return result

converted = convert_to_percent_change(data)

new_path = os.path.join('backtest', 'GPT_formatted.json')
with open(new_path, 'w') as file:
    json.dump(converted, file, indent=4)
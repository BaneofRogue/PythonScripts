import json
import os
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go

# Load data
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'spy_ema.json')
with open(json_path) as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)
df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')

# Bounce detection function
def detect_ema_bounces(candles, ema_key='ema21', lookahead=2, min_pct_gain=0.0, tolerance_pct=None, tolerance_abs=None):
    """
    Detect EMA bounces where:
    - candle low OR close is within a tolerance (absolute or % based) below the EMA value
    - a future close (within lookahead) exceeds the EMA
    - the price has gained at least min_pct_gain % from the bounce low

    :param candles: List of dicts with OHLC and EMA values
    :param ema_key: Key for the EMA (e.g. 'ema21')
    :param lookahead: How many candles ahead to check for confirmation
    :param min_pct_gain: % gain required from bounce low to future close
    :param tolerance_pct: Allowed % below EMA to still count as a bounce (e.g., 0.1 = 0.1%)
    :param tolerance_abs: Allowed absolute $ below EMA to count as a bounce (e.g., 0.3 = 30 cents)
    :return: List of bounce events
    """
    if tolerance_pct is None and tolerance_abs is None:
        raise ValueError("Must specify either tolerance_pct or tolerance_abs")

    bounces = []
    for i in range(len(candles) - lookahead):
        curr = candles[i]
        if ema_key not in curr or 'low' not in curr or 'close' not in curr:
            continue

        ema_val = curr[ema_key]
        low = curr['low']
        close = curr['close']

        def within_tolerance(price):
            diff = ema_val - price
            if tolerance_pct is not None and 0 <= (diff / ema_val) * 100 <= tolerance_pct:
                return True
            if tolerance_abs is not None and 0 <= diff <= tolerance_abs:
                return True
            return False

        # Check if low OR close is within tolerance below EMA
        if within_tolerance(low) or within_tolerance(close):
            for j in range(1, lookahead + 1):
                future = candles[i + j]
                if 'close' not in future or ema_key not in future:
                    continue
                gain_pct = ((future['close'] - low) / low) * 100
                if future['close'] > future[ema_key] and gain_pct >= min_pct_gain:
                    bounces.append({
                        'timestamp': curr['timestamp'],
                        'datetime': datetime.fromtimestamp(curr['timestamp']),
                        'price': low,
                        'ema': ema_key.upper()
                    })
                    break
    return bounces


# Detect bounces
bounces_all = []
for ema_key in ['ema21', 'ema50', 'ema100', 'ema200']:
    bounces = detect_ema_bounces(data, ema_key=ema_key, lookahead=5, min_pct_gain=1.0, tolerance_pct=0.2)
    bounces_all.extend(bounces)

# Create chart
fig = go.Figure(data=[go.Candlestick(
    x=df['datetime'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Price'
)])

# Add EMA lines
for ema in ['ema21', 'ema50', 'ema100', 'ema200']:
    fig.add_trace(go.Scatter(
        x=df['datetime'],
        y=df[ema],
        mode='lines',
        name=ema.upper()
    ))

# Add bounce markers
ema_colors = {
    'EMA21': 'red',
    'EMA50': 'blue',
    'EMA100': 'orange',
    'EMA200': 'green'
}

for ema in ['EMA21', 'EMA50', 'EMA100', 'EMA200']:
    b_df = pd.DataFrame([b for b in bounces_all if b['ema'] == ema])
    if not b_df.empty:
        fig.add_trace(go.Scatter(
            x=b_df['datetime'],
            y=b_df['price'],
            mode='markers',
            name=f'Bounce {ema}',
            marker=dict(
                symbol='triangle-down',
                size=10,
                color=ema_colors[ema]
            )
        ))

# Final layout
fig.update_layout(
    title='SPY Candlestick with EMA Bounces',
    xaxis_title='Date',
    yaxis_title='Price',
    xaxis_rangeslider_visible=False
)

# Show chart
fig.show()
input()

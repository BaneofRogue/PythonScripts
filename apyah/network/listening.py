import json

from DrissionPage import Chromium

# Step 1: Launch Chromium and get the latest tab
browser = Chromium()
tab = browser.latest_tab

# Step 2: Navigate to the Webull screener URL
# (Change this to the actual screener page URL)
webull_screener_url = 'https://app.webull.com/screener'
tab.get(webull_screener_url)

# Step 3: Start listening - match the expected domain or API path
# You'll need to inspect DevTools (F12) -> Network tab -> XHR / WS 
# For example, "/quote/tickerList" or "screener" in the URL
tab.listen.start(targets=['getQuote?tickerId='], is_regex=False)

print("🎧 Listening for data packets... Press Ctrl+C to stop.")

try:
    # Step 4: Continuously capture and print packets
    for packet in tab.listen.steps():
        print(f"\n📦 URL: {packet.url}")
        print(f"Method: {packet.method}")
        print(f"Resource Type: {packet.resourceType}")
        
        # If the response body is JSON, pretty print it
        try:
            data = packet.response.body
            if isinstance(data, dict):
                print("📊 Data:")
                print(json.dumps(data, indent=2))
            else:
                print("📄 Raw response:")
                print(data)
        except Exception as e:
            print(f"❌ Error reading response: {e}")

except KeyboardInterrupt:
    print("\n🛑 Stopped listening.")

finally:
    tab.listen.stop()

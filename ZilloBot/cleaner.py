import json
import os


def clean_data():
    file_path = "packets_0.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        body = data[0]['body']
        
        results = body.get("cat1", {}).get("searchResults", {}).get("mapResults", [])
        print(f"Found {len(results)} items inside of mapResults")

        for item in results:
            print(f"Cleaning item with zpid: {item.get('zpid', 'N/A')}")
            item.pop("imgSrc", None)
            item.pop("hasImage", None)
            item.pop("latLong", None)
            item.pop("canSaveBuilding", None)
            item.pop("isFavorite", None)
            item.pop("has3DModel", None)
            item.pop("priceLabel", None)
            
            hpData = item.get("hpData", {}).get("homeInfo", {})
            if hpData:
                print(f"Cleaning hpData for item with zpid: {hpData.get('zpid', 'N/A')}")
                hpData.pop("isFeatured", None)
                hpData.pop("shouldHighlight", None)
                hpData.pop("shouldHighlight", None)
                hpData.pop("shouldHighlight", None)
                hpData.pop("shouldHighlight", None)
            
        with open("cleaned_body.json", "w") as f:
            json.dump(body, f, indent=2)
            
clean_data()
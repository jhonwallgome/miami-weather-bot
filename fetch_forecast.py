import requests
import json
from datetime import datetime
import os

def fetch_miami_forecast():
    # Miami coordinates
    lat, lon = 25.7617, -80.1918
    
    print(f"Fetching forecast for Miami at {datetime.utcnow().isoformat()}")
    
    # NWS API requires a User-Agent header
    headers = {
        'User-Agent': '(Miami Weather Bot, your-email@example.com)',
        'Accept': 'application/json'
    }
    
    try:
        # Step 1: Get grid point data
        point_url = f"https://api.weather.gov/points/{lat},{lon}"
        print(f"Getting grid point from: {point_url}")
        
        response = requests.get(point_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Step 2: Get forecast URL
        forecast_url = data['properties']['forecast']
        print(f"Getting forecast from: {forecast_url}")
        
        # Step 3: Fetch detailed forecast
        forecast_response = requests.get(forecast_url, headers=headers, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        # Step 4: Load existing forecasts
        os.makedirs('data', exist_ok=True)
        filepath = 'data/forecasts.json'
        
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                all_forecasts = json.load(f)
        else:
            all_forecasts = []
        
        # Step 5: Add new forecast with timestamp
        new_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'location': 'Miami, FL',
            'coordinates': {'lat': lat, 'lon': lon},
            'forecast': forecast_data['properties']['periods'][:7]  # Next 7 periods
        }
        
        all_forecasts.append(new_entry)
        
        # Keep only last 200 forecasts (about 2 weeks of data)
        all_forecasts = all_forecasts[-200:]
        
        # Step 6: Save to file
        with open(filepath, 'w') as f:
            json.dump(all_forecasts, f, indent=2)
        
        print(f"✓ Successfully saved forecast! Total forecasts stored: {len(all_forecasts)}")
        print(f"✓ Latest forecast: {new_entry['forecast'][0]['name']} - {new_entry['forecast'][0]['shortForecast']}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching forecast: {e}")
        raise
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        raise

if __name__ == '__main__':
    fetch_miami_forecast()
  

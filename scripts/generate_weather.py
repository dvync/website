import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Calculate dynamic date range
start_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")

print(f"Fetching weather data from {start_date} to {end_date}")

url = f"https://archive-api.open-meteo.com/v1/archive?latitude=39.77&longitude=-86.16&daily=temperature_2m_max,temperature_2m_min&start_date={start_date}&end_date={end_date}&temperature_unit=fahrenheit&timezone=America/Indiana/Indianapolis"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if "daily" not in data:
        print(f"Error: Unexpected API response: {data}")
        sys.exit(1)
    
    print(f"Received data for {len(data['daily']['time'])} days")
    
    df = pd.DataFrame(data["daily"])
    
    # Save to the same location your website already expects
    # Use absolute path so it works whether run from scripts/ or root directory
    script_dir = Path(__file__).parent
    output_path = script_dir.parent / "data" / "daily_weather_report.csv"
    
    # Create data directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(output_path, index=False)
    
    print(f"✓ Weather CSV successfully written to {output_path}")
    print(f"Data preview:")
    print(df.to_string())
    
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error processing weather data: {e}")
    sys.exit(1)
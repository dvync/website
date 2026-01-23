import requests
import pandas as pd
from datetime import datetime, timedelta

# Calculate dynamic date range
start_date = (datetime.today() - timedelta(days=8)).strftime("%Y-%m-%d")
end_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

url = f"https://archive-api.open-meteo.com/v1/archive?latitude=39.77&longitude=-86.16&daily=temperature_2m_max,temperature_2m_min&start_date={start_date}&end_date={end_date}&temperature_unit=fahrenheit&timezone=America/Indiana/Indianapolis"

data = requests.get(url).json()

df = pd.DataFrame(data["daily"])

# Save to the same location your website already expects
output_path = "../data/daily_weather_report.csv"

df.to_csv(output_path, index=False)

print(f"Weather CSV written to {output_path}")
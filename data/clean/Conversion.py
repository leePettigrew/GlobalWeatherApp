#Conversion for mongo

import pandas as pd

# Load your CSV data
df = pd.read_csv('global_weather_cleaned.csv')

# Convert DataFrame to JSON
df.to_json('global_weather_cleaned.csv.json', orient='records')

#nevermind, mongo works fine with csv files

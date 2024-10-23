# data_processing.py

import pandas as pd
import numpy as np
import os

# Define the base directory (parent directory of 'scripts')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths to data directories
raw_data_dir = os.path.join(base_dir, 'data', 'raw')
clean_data_dir = os.path.join(base_dir, 'data', 'clean')

# Define file paths for input and output files
raw_data_file = os.path.join(raw_data_dir, 'GlobalWeatherRepository.csv')
clean_data_file = os.path.join(clean_data_dir, 'global_weather_cleaned.csv')

# Load the raw dataset into a pandas DataFrame
try:
    df = pd.read_csv(raw_data_file)
    print("Raw data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {raw_data_file} does not exist.")
    exit()

# Display initial dataset information
print("\nInitial Dataset Information:")
print(df.info())

# Display first few rows
print("\nFirst 5 rows:")
print(df.head())

# Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Rename columns to have consistent naming conventions
df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)

# Display updated column names
print("\nUpdated Column Names:")
print(df.columns.tolist())

# Convert 'last_updated' to datetime if it exists in the dataset
if 'last_updated' in df.columns:
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    print("\n'last_updated' column converted to datetime format.")
else:
    print("Column 'last_updated' not found.")

# Drop unnecessary columns to simplify the dataset
columns_to_drop = [
    'temperature_fahrenheit', 'feels_like_fahrenheit', 'pressure_in',
    'precip_in', 'visibility_miles'
]
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Display remaining columns
print("\nColumns after dropping unnecessary ones:")
print(df.columns.tolist())

# List of numerical columns to ensure they have correct data types
numerical_cols = [
    'latitude', 'longitude', 'temperature_celsius', 'wind_mph', 'wind_kph',
    'wind_degree', 'pressure_mb', 'precip_mm', 'humidity', 'cloud',
    'feels_like_celsius', 'visibility_km', 'uv_index', 'gust_mph', 'gust_kph',
    'air_quality_carbon_monoxide', 'air_quality_ozone',
    'air_quality_nitrogen_dioxide', 'air_quality_sulphur_dioxide',
    'air_quality_pm2.5', 'air_quality_pm10', 'air_quality_us-epa-index',
    'air_quality_gb-defra-index', 'moon_illumination'
]

# Convert numerical columns to appropriate types
for col in numerical_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Check data types after conversion
print("\nData Types of Numerical Columns:")
print(df[numerical_cols].dtypes)

# Check for NaN values after type conversion
print("\nMissing values after type conversion:")
print(df[numerical_cols].isnull().sum())

# Drop rows with NaN values in critical columns for analysis
key_columns = ['temperature_celsius', 'humidity']
df.dropna(subset=key_columns, inplace=True)
df.reset_index(drop=True, inplace=True)

# Standardize text columns for consistency
text_columns = ['condition_text', 'wind_direction', 'country', 'location_name']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].str.lower().str.strip()

# Ensure the clean data directory exists before saving
if not os.path.exists(clean_data_dir):
    os.makedirs(clean_data_dir)

# Save the cleaned DataFrame to a CSV file
df.to_csv(clean_data_file, index=False)
print(f"\nCleaned data saved to {clean_data_file}")

# Display a summary of key statistics for temperature and humidity
temp_mean = df['temperature_celsius'].mean()
temp_max = df['temperature_celsius'].max()
temp_min = df['temperature_celsius'].min()
print(f"\nTemperature (Celsius) - Mean: {temp_mean:.2f}, Max: {temp_max}, Min: {temp_min}")

humidity_mean = df['humidity'].mean()
humidity_max = df['humidity'].max()
humidity_min = df['humidity'].min()
print(f"Humidity (%) - Mean: {humidity_mean:.2f}, Max: {humidity_max}, Min: {humidity_min}")

# Display final dataset information for verification
print("\nCleaned Dataset Information:")
print(df.info())

# Display first few rows of the cleaned data to verify changes
print("\nFirst 5 rows of cleaned data:")
print(df.head())

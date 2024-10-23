# data_analysis.py

# Import libraries for data analysis and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define the base directory (parent directory of 'scripts')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the path to the cleaned data file
clean_data_file = os.path.join(base_dir, 'data', 'clean', 'global_weather_cleaned.csv')

# Define the path to save figures
figures_dir = os.path.join(base_dir, 'figures')

# Ensure the figures directory exists
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

# Load the cleaned dataset into a pandas DataFrame
try:
    df = pd.read_csv(clean_data_file)
    print("Cleaned data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {clean_data_file} does not exist.")
    exit()

# Display initial dataset information
print("\nDataset Information:")
print(df.info())

# Generate summaries
# Sort the dataset by temperature_celsius in descending order
df_sorted = df.sort_values(by='temperature_celsius', ascending=False)

# Top 5 hottest locations
top5_hottest = df_sorted[['country', 'location_name', 'temperature_celsius']].head(5)
print("\nTop 5 Hottest Locations:")
print(top5_hottest)

# Top 5 coldest locations
top5_coldest = df_sorted[['country', 'location_name', 'temperature_celsius']].tail(5)
print("\nTop 5 Coldest Locations:")
print(top5_coldest)

# Group by 'country' and calculate the average temperature
country_avg_temp = df.groupby('country')['temperature_celsius'].mean().reset_index()

# Sort by average temperature
country_avg_temp_sorted = country_avg_temp.sort_values(by='temperature_celsius', ascending=False)
print("\nAverage Temperature by Country (Top 10):")
print(country_avg_temp_sorted.head(10))

# Plot a histogram of temperatures
plt.figure(figsize=(10, 6))
sns.histplot(df['temperature_celsius'], bins=30, kde=True, color='royalblue')
plt.title('Distribution of Global Temperatures')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.tight_layout()

# Save the figure
histogram_path = os.path.join(figures_dir, 'temperature_histogram.png')
plt.savefig(histogram_path)
plt.show()

# Convert 'last_updated' to datetime if necessary
if not np.issubdtype(df['last_updated'].dtype, np.datetime64):
    df['last_updated'] = pd.to_datetime(df['last_updated'])

# Filter data for a specific country (e.g., India)
country_name = 'india'
df_country = df[df['country'].str.lower() == country_name]

# Check if the DataFrame is not empty
if not df_country.empty:
    # Sort data by date
    df_country = df_country.sort_values(by='last_updated')

    # Plot temperature over time
    plt.figure(figsize=(15, 7))
    plt.plot(df_country['last_updated'], df_country['temperature_celsius'], marker='o', linestyle='-', color='tomato')
    plt.title(f'Temperature Changes Over Time in {country_name.title()}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save the figure
    line_graph_path = os.path.join(figures_dir, f'{country_name}_temperature_over_time.png')
    plt.savefig(line_graph_path)
    plt.show()
else:
    print(f"No data available for country: {country_name}")

# Additional visualization - Top 10 locations with the highest precipitation
top10_precip = df.sort_values(by='precip_mm', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='location_name', y='precip_mm', data=top10_precip, palette='Blues_d')
plt.title('Top 10 Locations with Highest Precipitation')
plt.xlabel('Location')
plt.ylabel('Precipitation (mm)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
precip_path = os.path.join(figures_dir, 'top10_highest_precipitation.png')
plt.savefig(precip_path)
plt.show()

# Average wind speed by country
country_avg_wind = df.groupby('country')['wind_kph'].mean().reset_index()
top10_wind_countries = country_avg_wind.sort_values(by='wind_kph', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='country', y='wind_kph', data=top10_wind_countries, palette='coolwarm')
plt.title('Top 10 Countries with Highest Average Wind Speed')
plt.xlabel('Country')
plt.ylabel('Average Wind Speed (kph)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
wind_path = os.path.join(figures_dir, 'top10_avg_wind_speed.png')
plt.savefig(wind_path)
plt.show()

# Line Plot of Average Daily Temperature Globally
df['date'] = df['last_updated'].dt.date
avg_temp_per_day = df.groupby('date')['temperature_celsius'].mean().reset_index()

plt.figure(figsize=(14, 7))
plt.plot(avg_temp_per_day['date'], avg_temp_per_day['temperature_celsius'], marker='o', color='royalblue')
plt.title('Average Global Temperature per Day')
plt.xlabel('Date')
plt.ylabel('Average Temperature (°C)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the figure
avg_temp_path = os.path.join(figures_dir, 'avg_global_temp_per_day.png')
plt.savefig(avg_temp_path)
plt.show()

# Optional: Bar chart of average humidity by country
country_avg_humidity = df.groupby('country')['humidity'].mean().reset_index()
top10_humid_countries = country_avg_humidity.sort_values(by='humidity', ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(x='country', y='humidity', data=top10_humid_countries, palette='viridis')
plt.title('Top 10 Countries with Highest Average Humidity')
plt.xlabel('Country')
plt.ylabel('Average Humidity (%)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
humidity_path = os.path.join(figures_dir, 'top10_humid_countries.png')
plt.savefig(humidity_path)
plt.show()

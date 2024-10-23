# data_exploration.py

# Import libraries needed for data handling, numerical operations, and visualization.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set up base directory to ensure file paths are correct relative to the script.
# This will help locate the raw data file no matter where the script is run from.
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the path to the raw data file for easy access later in the script.
raw_data_file = os.path.join(base_dir, 'data', 'raw', 'GlobalWeatherRepository.csv')

# Load the raw dataset into a pandas DataFrame.
# Using try-except to handle the case where the file might be missing or incorrectly placed.
try:
    df = pd.read_csv(raw_data_file)
    print("Raw data loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file {raw_data_file} does not exist.")
    exit()

# Explanation for choosing this dataset:
# This dataset includes a wide range of weather data from various global locations.
# It contains data points like temperature, humidity, and precipitation over time, making it perfect
# for analyzing weather trends and patterns on a global scale. Its coverage and time depth allow for
# robust analysis and potential predictions.

# Displaying the first few rows to get a sense of how the data is structured.
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Print the dataset dimensions to understand its size.
print(f"\nDataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

# List out all the column names to get a quick overview of what features are available.
print("\nColumn names:")
print(df.columns.tolist())

# Checking the data types of each column to identify if any adjustments are needed.
print("\nData types of each column:")
print(df.dtypes)

# Checking for missing values across the dataset to understand data quality.
print("\nMissing values in each column:")
print(df.isnull().sum())

# Using a heatmap to visualize where missing values are present in the dataset.
# This provides a visual representation of missing data.
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Heatmap of Missing Values')
plt.show()

# Generating summary statistics for numerical columns to understand the data's central tendencies.
print("\nStatistical summary of numerical columns:")
print(df.describe())

# Identifying which columns contain categorical data for further analysis.
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
print("\nCategorical columns:")
print(categorical_cols)

# Displaying the unique values in each categorical column to understand possible categories.
for col in categorical_cols:
    print(f"\nUnique values in '{col}': {df[col].nunique()}")
    print(df[col].unique())

# Plotting the distribution of temperature to see how temperatures are spread across the dataset.
# Using histograms for a clear understanding of the distribution.
if 'temperature' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['temperature'].dropna(), kde=True)
    plt.title('Distribution of Temperature')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("Column 'temperature' not found in the dataset.")

# Similar plot for humidity to analyze its distribution.
if 'humidity' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df['humidity'].dropna(), kde=True)
    plt.title('Distribution of Humidity')
    plt.xlabel('Humidity (%)')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("Column 'humidity' not found in the dataset.")

# Calculating the correlation matrix to see how numerical variables relate to each other.
# This helps identify any strong correlations that could be interesting for analysis.
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr_matrix = df[numerical_cols].corr()

# Displaying the correlation matrix for review.
print("\nCorrelation matrix:")
print(corr_matrix)

# Visualizing the correlation matrix using a heatmap for easier interpretation of relationships.
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Analyzing temperature over time if a date column exists.
# This will help identify trends or patterns in temperature over the recorded time period.
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])  # Converting the date column to a datetime format.

    # Setting the 'date' column as the index to make time-based plotting easier.
    df.set_index('date', inplace=True)

    # Plotting the temperature values over time to visualize any trends.
    if 'temperature' in df.columns:
        plt.figure(figsize=(15, 7))
        df['temperature'].plot()
        plt.title('Temperature Over Time')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.show()
    else:
        print("Column 'temperature' not found for time series analysis.")
else:
    print("Column 'date' not found in the dataset.")

# If the dataset includes latitude and longitude, we can plot data points on a map.
# This allows us to see where the data points are geographically distributed.
if 'latitude' in df.columns and 'longitude' in df.columns:
    # Using a sample to avoid overplotting.
    df_sample = df.sample(n=1000, random_state=42)

    # Plotting the latitude and longitude to visualize geographical distribution.
    plt.figure(figsize=(12, 6))
    plt.scatter(df_sample['longitude'], df_sample['latitude'], alpha=0.5)
    plt.title('Geographical Distribution of Data Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
else:
    print("Latitude and longitude columns not found for geographical analysis.")

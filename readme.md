# Global Weather Data Analysis and Visualization Project

## Table of Contents
- [Project Overview](#project-overview)
- [Dataset Justification](#dataset-justification)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Virtual Environment](#2-set-up-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [Instructions to Run the Project Locally](#instructions-to-run-the-project-locally)
  - [1. Data Processing](#1-data-processing)
  - [2. Data Analytics and Visualization](#2-data-analytics-and-visualization)
  - [3. Kafka Producer and Consumer](#3-kafka-producer-and-consumer)
  - [4. Database Operations](#4-database-operations)
    - [MySQL Operations](#mysql-operations)
    - [MongoDB Operations](#mongodb-operations)
  - [5. Streamlit Web Application](#5-streamlit-web-application)
- [Hosted Streamlit App](#hosted-streamlit-app)
- [File Descriptions](#file-descriptions)
- [Additional Notes](#additional-notes)
- [Credits](#credits)
- [Contact Information](#contact-information)

## Project Overview
This project is a full-stack data science application that involves data processing, data analytics, Kafka-based data streaming, database operations, and hosting a web application using Streamlit. The application uses the Global Weather Dataset to perform weather-related analysis and predictions on a global scale.

## Dataset Justification
The Global Weather Dataset from Kaggle provides comprehensive weather data for multiple global locations. It includes various meteorological parameters such as temperature, humidity, precipitation, and more. This dataset is suitable for weather-related analysis and predictions because:

- **Global Coverage**: It covers a wide range of geographical locations, allowing for global-scale analysis.
- **Detailed Metrics**: It includes detailed weather metrics necessary for in-depth analysis.
- **Data Volume**: The dataset is large and diverse, which helps in building robust predictive models.


## Project Overview
This project is a full-stack data science application that involves data processing, data analytics, Kafka-based data streaming, database operations, and hosting a web application using Streamlit. The application uses the Global Weather Dataset to perform weather-related analysis and predictions on a global scale.

### Project Structure
```
GlobalWeatherApp/
│
├── .venv/                                # Virtual environment for managing dependencies
│
├── data/                                 # Directory containing data files
│   ├── clean/                            # Processed data files
│   │   ├── Conversion.py                 # Script for data conversion and cleaning
│   │   ├── global_weather_cleaned.csv    # Cleaned weather data in CSV format
│   │   └── global_weather_cleaned.csv.json # Cleaned data in JSON format
│   ├── raw/                              # Raw data files before processing
│   │   ├── GlobalWeatherRepository.csv   # Original dataset
│   │   └── consumed_data.csv             # Data processed and consumed for Kafka streaming
│
├── figures/                              # Directory for generated visualizations
│   ├── india_temperature_over_time.png   # Temperature trends in India over time
│   ├── temperature_histogram.png         # Histogram of temperature distribution
│   └── top10_humid_countries.png         # Top 10 countries with the highest humidity levels
│
├── scripts/                              # Python scripts for different functionalities
│   ├── data_analysis.py                  # Script for analyzing weather data
│   ├── data_exploration.py               # Script for initial data exploration
│   ├── data_processing.py                # Script for data cleaning and preparation
│   ├── kafka_consumer.py                 # Kafka consumer script for streaming data
│   ├── kafka_producer.py                 # Kafka producer script for sending data
│   └── docker-compose.yml                # Docker Compose file for setting up services
│
├── readme.md                             # Documentation file for the project
└── requirements.txt                      # List of Python dependencies for the project
```

## Prerequisites
- Python 3.7+
- MySQL Server
- MySQL Workbench
- MongoDB Server
- MongoDB Compass
- Apache Kafka
- Docker desktop
- Git

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your_username/GlobalWeatherDataProject.git
cd GlobalWeatherDataProject
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment(Not entirely necessary, but recommended):

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Instructions to Run the Project Locally

### 1. Data Exploration
**Script:** `scripts/data_exploration.py`

**Steps:**
- Load the raw dataset from `data/raw/GlobalWeatherRepository.csv`.
- Perform initial data exploration to understand the data structure.
- Generate summary statistics and identify missing values.
- Visualize basic relationships in the data.
- Save exploratory plots in `figures/`.

**Run:**
```bash
python scripts/data_exploration.py
```

### 2. Data Processing
**Script:** `scripts/data_processing.py`

**Steps:**
- Clean the dataset (handle missing values, convert data types).
- Transform data as necessary for analysis.
- Store the cleaned data in `data/clean/global_weather_cleaned.csv`.
- Convert cleaned data to JSON format for MongoDB import.

**Run:**
```bash
python scripts/data_processing.py
```

### 3. Data Analysis and Visualization
**Script:** `scripts/data_analysis.py`

**Steps:**
- Analyze the cleaned dataset to extract insights.
- Perform analyses such as finding the top 5 hottest and coldest locations.
- Group data by relevant fields and compute statistics.
- Generate advanced visualizations and save them in `figures/`.

**Run:**
```bash
python scripts/data_analysis.py
```

### 4. Kafka Producer and Consumer

#### Set Up Kafka Services
Start Zookeeper and Kafka server. If you are using Docker Compose, you can use the provided `docker-compose.yml` file.

```bash
docker-compose up -d
```

Alternatively, start Kafka and Zookeeper manually.

#### Kafka Producer
**Script:** `scripts/kafka_producer.py`

**Steps:**
- Simulate real-time weather updates.
- Send data points every second to the Kafka topic `global_weather`.

**Run:**
```bash
python scripts/kafka_producer.py
```

#### Kafka Consumer
**Script:** `scripts/kafka_consumer.py`

**Steps:**
- Listen to the `global_weather` topic.
- Log consumed data to `data/raw/consumed_data.csv`.
- Display a summary after receiving data.

**Run:**
```bash
python scripts/kafka_consumer.py
```

### 5. Database Operations

#### MySQL Operations

**Setup:**
- Install MySQL Server and MySQL Workbench.

**Create a New Database:**
- Open MySQL Workbench.
- Create a new connection if not already connected.
- Open a new SQL tab and run:
  
  ```sql
  CREATE DATABASE GlobalWeatherDB;
  USE GlobalWeatherDB;
  ```

**Create the WeatherData Table:**
- Use the SQL script provided in `queries/create_table.sql` or create the table using the commands provided.

**Import the Cleaned Dataset:**
- Use the Table Data Import Wizard:
  - Right-click on the `WeatherData` table and select "Table Data Import Wizard".
  - Follow the prompts to import `data/clean/global_weather_cleaned.csv`.

**Run SQL Queries:**
- Open a new SQL tab.
- Copy and paste queries from `queries/sql_queries.txt`.
- Execute the queries to perform data retrieval and analysis.

#### MongoDB Operations

**Setup:**
- Install MongoDB Server and MongoDB Compass.
- Start MongoDB Server.

**Create a New Database and Collection:**
- Open MongoDB Compass.
- Click "Create Database".
- Name the database `GlobalWeatherDB` and the collection `GlobalWeatherData`.

**Import the Cleaned Dataset:**
- Use MongoDB Compass to import `data/clean/global_weather_cleaned.csv.json` into `GlobalWeatherData`.

**Run MongoDB Queries:**
- Use the Filter and Sort fields in MongoDB Compass.
- Copy queries from `queries/mongodb_queries.txt`.

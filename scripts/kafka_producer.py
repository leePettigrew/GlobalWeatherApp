# kafka_producer.py

import os
import time
import json
import pandas as pd
from confluent_kafka import Producer

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the cleaned data file
clean_data_file = os.path.join(base_dir, 'data', 'clean', 'global_weather_cleaned.csv')

df = pd.read_csv(clean_data_file)

# Check if the DataFrame is not empty
if df.empty:
    print("DataFrame is empty. Please check the data file.")
    exit()

producer_conf = {
    'bootstrap.servers': 'localhost:9092'
}

# Create a Producer instance
producer = Producer(producer_conf)

# Convert the DataFrame to a list of dictionaries
data_records = df.to_dict(orient='records')

# Define the Kafka topic to send data to
topic_name = 'global_weather'

print("Starting Kafka Producer...")

try:
    # Iterate over each record in the data
    for record in data_records:
        # Convert the record dictionary to a JSON string
        record_value = json.dumps(record)

        producer.produce(topic=topic_name, value=record_value)

        producer.flush()

        print(f"Sent: {record}")

        time.sleep(1)
except KeyboardInterrupt:
    print("Producer stopped manually.")
finally:
    producer.flush()
    print("Kafka Producer closed.")

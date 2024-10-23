# kafka_producer.py

import os
import time
import json
import pandas as pd
from confluent_kafka import Producer

# Define the base directory (parent directory of 'scripts')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the cleaned data file
clean_data_file = os.path.join(base_dir, 'data', 'clean', 'global_weather_cleaned.csv')

# Load the cleaned dataset into a pandas DataFrame
df = pd.read_csv(clean_data_file)

# Check if the DataFrame is not empty
if df.empty:
    print("DataFrame is empty. Please check the data file.")
    exit()

# Kafka Producer configuration
# 'bootstrap.servers' specifies the Kafka broker address
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

        # Send the data to the Kafka topic
        # 'value' is the message content
        producer.produce(topic=topic_name, value=record_value)

        # Flush the producer buffer to ensure the message is sent
        producer.flush()

        # Print confirmation
        print(f"Sent: {record}")

        # Sleep for 1 second to simulate real-time data streaming
        time.sleep(1)
except KeyboardInterrupt:
    # Handle manual interruption (Ctrl+C)
    print("Producer stopped manually.")
finally:
    # Flush any remaining messages and close the producer
    producer.flush()
    print("Kafka Producer closed.")

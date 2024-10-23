# kafka_consumer.py

import os
import json
import pandas as pd
from confluent_kafka import Consumer, KafkaException

# Define the base directory (parent directory of 'scripts')
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to save the consumed data
consumed_data_file = os.path.join(base_dir, 'data', 'consumed_data.csv')

# Kafka Consumer configuration
# 'bootstrap.servers' specifies the Kafka broker address
# 'group.id' assigns the consumer to a group
# 'auto.offset.reset' defines where to start reading messages
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'weather-consumers',
    'auto.offset.reset': 'earliest'
}

# Create a Consumer instance
consumer = Consumer(consumer_conf)

# Subscribe to the Kafka topic
topic_name = 'global_weather'
consumer.subscribe([topic_name])

# List to store consumed records
consumed_records = []

print("Starting Kafka Consumer...")

try:
    # Continuously poll for new messages
    while True:
        # Poll messages from Kafka
        # Timeout is set to 1 second
        msg = consumer.poll(1.0)

        if msg is None:
            # No message received within the timeout
            continue
        if msg.error():
            # Handle any errors
            print(f"Consumer error: {msg.error()}")
            continue

        # Decode the message value from bytes to string
        record_value = msg.value().decode('utf-8')

        # Convert the JSON string back to a dictionary
        record = json.loads(record_value)
        print(f"Received: {record}")

        # Add the record to the list
        consumed_records.append(record)

        # Stop after receiving 60 records
        if len(consumed_records) >= 60:
            print("Received 60 records. Stopping consumer.")
            break
except KeyboardInterrupt:
    # Handle manual interruption (Ctrl+C)
    print("Consumer stopped manually.")
except KafkaException as e:
    # Handle Kafka-specific exceptions
    print(f"Kafka error: {e}")
finally:
    # Close the consumer to commit final offsets and clean up
    consumer.close()
    print("Kafka Consumer closed.")

    # Check if any records were consumed
    if consumed_records:
        # Convert the list of records to a DataFrame
        df_consumed = pd.DataFrame(consumed_records)

        # Save the consumed records to a CSV file
        df_consumed.to_csv(consumed_data_file, index=False)
        print(f"Consumed data saved to {consumed_data_file}")

        # Display summary statistics
        print("\nSummary of Consumed Data:")

        # Calculate temperature statistics if available
        if 'temperature_celsius' in df_consumed.columns:
            temp_mean = df_consumed['temperature_celsius'].mean()
            temp_max = df_consumed['temperature_celsius'].max()
            temp_min = df_consumed['temperature_celsius'].min()
            print(f"Temperature (Celsius) - Mean: {temp_mean:.2f}, Max: {temp_max}, Min: {temp_min}")
        else:
            print("Temperature data not available.")

        # Calculate humidity statistics if available
        if 'humidity' in df_consumed.columns:
            humidity_mean = df_consumed['humidity'].mean()
            humidity_max = df_consumed['humidity'].max()
            humidity_min = df_consumed['humidity'].min()
            print(f"Humidity (%) - Mean: {humidity_mean:.2f}, Max: {humidity_max}, Min: {humidity_min}")
        else:
            print("Humidity data not available.")
    else:
        print("No records were consumed.")

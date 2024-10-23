from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from confluent_kafka import Consumer
import pandas as pd
import json
import threading

app = Flask(__name__)
CORS(app)

# Load the cleaned data
df = pd.read_csv('../data/clean/global_weather_cleaned.csv')

@app.route('/data', methods=['GET'])
def get_data():
    # Apply filters if provided
    country = request.args.get('country')
    date = request.args.get('date')
    filtered_df = df.copy()
    if country:
        filtered_df = filtered_df[filtered_df['country'] == country]
    if date:
        filtered_df = filtered_df[filtered_df['last_updated'].str.contains(date)]
    data = filtered_df.to_dict(orient='records')
    return jsonify(data)

# Endpoint to stream data from Kafka
@app.route('/stream')
def stream():
    def generate():
        # Kafka consumer configuration
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'weather_group',
            'auto.offset.reset': 'latest',
        }
        consumer = Consumer(conf)
        consumer.subscribe(['global_weather'])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    continue
                data = json.loads(msg.value().decode('utf-8'))
                yield f"data:{json.dumps(data)}\n\n"
        finally:
            consumer.close()

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)

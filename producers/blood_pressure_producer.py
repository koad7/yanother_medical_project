import csv
import time
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def read_csv_and_send_to_kafka(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            producer.send('health_data', value=row)
            time.sleep(1)  # simulate real-time data streaming

if __name__ == "__main__":
    csv_file = 'path_to_your_csv_file.csv'
    read_csv_and_send_to_kafka(csv_file)

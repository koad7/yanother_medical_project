import csv
import time
import socket
import json
from confluent_kafka import Producer

conf = {"bootstrap.servers": "kafka:9092", "client.id": socket.gethostname()}
producer = Producer(conf)


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        print("Message delivery failed: {}".format(err))
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))

def read_first_line_csv(filename):
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            first_line = next(reader)
            return first_line
    except FileNotFoundError:
        print("The file does not exist.")
    except StopIteration:
        print("The file is empty.")



def read_csv_and_send_to_kafka(csv_file):
    with open(csv_file, mode="r") as file:
        headers = set(read_first_line_csv(csv_file))
        headers = [header.strip() for header in headers]
        header_set = set(headers)

        reader = csv.DictReader(file)
        for row in reader:
            producer.produce(
                "blood_pressure",
                key=str(header_set),
                value=json.dumps(row),
                callback=delivery_report,
            )
            producer.poll(1)
            time.sleep(1)  # simulate real-time data streaming


if __name__ == "__main__":
    csv_file = "data/EDA.csv"
    read_csv_and_send_to_kafka(csv_file)
    # Wait for any outstanding messages to be delivered and report delivery 
    producer.flush()

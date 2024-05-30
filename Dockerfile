# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Kafka
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://archive.apache.org/dist/kafka/2.8.0/kafka_2.13-2.8.0.tgz && \
    tar -xvf kafka_2.13-2.8.0.tgz && \
    mv kafka_2.13-2.8.0 /usr/local/kafka

# Set environment variables
ENV KAFKA_HOME=/usr/local/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin

# Expose Kafka ports
EXPOSE 9092 2181

# Start Kafka and the producers
CMD ["sh", "-c", "bin/zookeeper-server-start.sh config/zookeeper.properties & bin/kafka-server-start.sh config/server.properties & python consumer/consumer.py"]

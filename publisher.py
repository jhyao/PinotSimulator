import six
import sys

# if sys.version_info >= (3, 12, 0):
sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
import requests
import socket
import random
import string
import json
import time
import datetime




producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

def generate_random_number():
    return random.randrange(0, 100000000)

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def get_time():
    return int(time.time() * 1000)

CONTENT_LENGTH=100
TOPIC = "issuerrisk"

def generate_record(id):
    record = {
        'UID': id,
        'UpdatedTime': get_time(),
        'Content': generate_random_string(CONTENT_LENGTH)
    }
    for i in range(1, 11):
        record[f'JTD{i}'] = generate_random_number()
    return json.dumps(record)

for i in range(3):
    for id in range(1_000_000):
        record = generate_record(id)
        producer.send(TOPIC, key=str(id).encode(), value=record.encode())
        if id % 10000 == 0:
            print(f'Published {i} round, {id} messages')
            producer.flush()

producer.flush()

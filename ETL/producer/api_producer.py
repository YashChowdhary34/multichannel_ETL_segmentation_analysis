from confluent_kafka import Producer
import requests
import time
import json

config = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(config)

def fetch_api_data():
  response = requests.get('api_link')
  return response.json()

def delivery_report(err, msg):
  if err is not None:
    print(f'Message delivery failed: {err}')
  else:
    print(f'Message delivered to {msg.topic()}')

while True:
  data = fetch_api_data()
  producer.produce(
    'api_source_topic',
    json.dumps(data).encode('utf-8'),
    callback=delivery_report
  )
  producer.poll(0)
  time.sleep(60) # poll every minute
import watchdog.observers import Observers
from watchdog.events import FileSystemEventHandler
from confluent_kafka import Producer

config = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(config)


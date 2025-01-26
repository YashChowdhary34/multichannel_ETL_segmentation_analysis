import psycopg2
from confluent_kafka import Producer

config = {'bootstrap.server': 'localhost:9092'}
producer = Producer(config)

def get_db_connection():
  return pycorpg2.connect(
    dbname='retail_db',
    user='posgres'
    password='password'
    host='localhost'
  )

def poll_database():
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute('SELECT * FROM retail_sales WHERE processed = FALSE')
  records = cursor.fetchall()
  #cdc logic
  return records

while True:
  records = poll_database()
  for records in records:
    producer.produce(
      'db_source_topic',
      str(record).encode('utf-8')
    )
  producer.flush()
  time.sleep(30)
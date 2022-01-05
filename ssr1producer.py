import requests
import pika
import pickle

MAX_PRIORITY = 100
TOTAL = 100
QUEUE_NAME = 'scrape2'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

for i in range(1, TOTAL + 1):
    url = 'https://ssr1.scrape.center/detail/{i}'
    request = requests.Request('Get', url)
    channel.basic_publish(exchange='',
                          routing_key=QUEUE_NAME,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                              content_type='application/json',
                              content_encoding='utf-8'
                          ),
                          body=pickle.dumps(request)
                          )
    print(f'Put request of {i}')

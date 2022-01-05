import requests
import pika
import pickle

MAX_PRIORITY = 100
QUEUE_NAME = 'scrape2'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
session = requests.Session()


def scrape_ssr1(request):
    try:
        response = session.send(request.prepare())
        print(f'success scrape {response.url}')
    except requests.RequestException:
        print(f'Error occurred when scraping {response.url}')


while True:
    method_frame, header, body = channel.basic_get(
        queue=QUEUE_NAME, auto_ack=True
    )
    if body:
        request = pickle.loads(body)
        print(f'Get {request}')
        scrape_ssr1(request)

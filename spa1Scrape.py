import requests
import logging
import pymongo

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'


def scrape_api(url):
    logging.info('scraping %s........')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


LIMIT = 10


def scrape_index(page):
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


DETAIL_RUL = 'https://spa1.scrape.center/api/movie/{id}'


def scrape_detail(id):
    url = DETAIL_RUL.format(id=id)
    return scrape_api(url)


TOTAL_PAGE = 10


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s', detail_data)
            sava_data(detail_data)
            logging.info('data save successfully')


MONGO_CONNECTION_STING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies'
MONGO_COLLECtION_NAME = 'movies'

client = pymongo.MongoClient(MONGO_CONNECTION_STING)
db = client['movies']
collection = db['movies']


def sava_data(data):
    collection.update_one({
        'name': data.get('name')
    }, {
        '$set': data
    }, upsert=True)


if __name__ == '__main__':
    main()

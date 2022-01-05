import logging
import asyncio
import aiohttp
import json
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_URL = 'https://spa5.scrape.center//api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/detail/{id}'
PAGE_SIZE = 18
PAGE_NUMBER = 100
CONCURRENCY = 5

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None


async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('scraping %s', url)
            async with session.get(url, ssl=False) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index(page):
    url = INDEX_URL.format(offset=PAGE_SIZE * (page - 1))
    return await scrape_api(url)


MONGO_CONNECTION_STING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECtION_NAME = 'books'

client = AsyncIOMotorClient(MONGO_CONNECTION_STING)
db = client[MONGO_DB_NAME]
collectiong = client[MONGO_COLLECtION_NAME]


async def save_data(data):
    logging.info('saving fdata %s', data)
    if data:
        return await collectiong.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


async def main():
    global session
    session = aiohttp.ClientSession()
    scrape_index_task = [asyncio.ensure_future(scrape_index(page)) for page in range(1, PAGE_NUMBER + 1)]
    result = await asyncio.gather(*scrape_index_task)
    logging.info('result %s', json.dumps(result, ensure_ascii=False, indent=2))
    ids = []
    for index_data in result:
        if not index_data: continue
        for item in index_data.get('result'):
            ids.append(item.get('id'))
    scrape_detail_task = [asyncio.ensure_future(scrape_detail(id) for id in ids)]
    await asyncio.wait(scrape_detail_task)
    await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

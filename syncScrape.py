import asyncio
import requests
import time
import aiohttp

start_time = time.time()


async def get_url(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await session.close()
    return response



async def request():
    url = 'https://www.httpbin.org/delay/5'
    print('Waiting for url', url)
    response = await get_url(url)
    print('Get response from', url, 'response', response)


tasks = [asyncio.ensure_future(request()) for _ in range(100)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end_time = time.time()
print('Cost Time:', end_time - start_time)

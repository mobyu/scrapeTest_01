import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq


async def main():
    browser = await launch(headless=False, args=['--disable-infobars'])
    page = await browser.newPage()
    await page.goto('https://spa2.scrape.center/')
    print('HTML:', await page.content())
    print('Cookies:', await page.cookies())
    await asyncio.sleep(5)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

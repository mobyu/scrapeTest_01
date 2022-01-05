import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False, userDataDir='./userdata',
                           args=['--disable-infobars'])
    page = await browser.newPage()
    await page.evaluateOnNewDocument('Object.defineProperty(navigator,"webdriver",{get: () => undefined})')
    await page.goto('https://www.taobao.com/')
    await asyncio.sleep(10)
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())

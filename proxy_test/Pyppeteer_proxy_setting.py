# 设置Pyppeteer代理

import asyncio
from pyppeteer import launch

proxy = '127.0.0.1'


# http协议
async def main():
    browser = await launch({'args': ['--proxy_server=http://' + proxy], 'headless': False})
    page = await browser.newPage()
    await page.goto('http://www.httpbin.org/get')
    print(await page.content())
    await browser.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

# socks代理，只需要将只要将协议换为socks5
# browser = await launch({'args': ['--proxy_server=socks5://' + proxy], 'headless': False})

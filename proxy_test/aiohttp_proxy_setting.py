# 为aiohttp设置代理

import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector

# http协议，无认证
proxy = 'http://127.0.0.1:7890'


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.httpbin.ort/get', proxy=proxy) as response:
            print(await response.text())


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

# http协议，需要认证，只需要将代理地址修改
# proxy = 'username:password@http://127.0.0.1:7890'


# 对于SOCKS代理，需要安装aiohttp-socks库
connector = ProxyConnector.from_url('socks5://127.0.0.1')


async def main2():
    async with aiohttp.ClientSession(connector=connector) as session2:
        async with session2.get('https://www.httpbin.org/get') as response2:
            print(await response2.text())

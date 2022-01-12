# 设置httpx代理
import httpx

proxy = '127.0.0.1:7890'
proxies = {
    'http://': 'http://' + proxy,
    'https://': 'http://' + proxy
}

with httpx.Client(proxies=proxies) as client:
    response = client.get('https://www.httpbin.org/get')
    print(response.text)

# 需要认证的代理
# proxy = 'username:password@127.0.0.1:7890'

# 对于socks代理需要使用httpx-socks[asyncio]库，同时设置同步或者异步模式

# 同步模式
from httpx_socks import SyncProxyTransport

transport1 = SyncProxyTransport.from_url('socks5://127.0.0.1:7891')

with httpx.Client(transport=transport1) as client1:
    response1 = client1.get('https://www.httpbin.org/get')
    print(response1.text)
# 异步模式
import asyncio
from httpx_socks import AsyncProxyTransport

transport2 = AsyncProxyTransport.from_url('socks5://127.0.0.1:7891')


async def main():
    async with httpx.Client(transport=transport2) as client2:
        response2 = await client2.get('https://www.httpbin.org/bin')
        print(response2.text)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

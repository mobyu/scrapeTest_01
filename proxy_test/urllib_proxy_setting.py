# urllib的代理设置
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
from urllib import request
import socks
import socket

# 基础代理服务

proxy1 = '127.0.0.1:7890'
proxy_handler1 = ProxyHandler({
    'http': 'http://' + proxy1,
    'https': 'https://' + proxy1
})
opener1 = build_opener(proxy_handler1)
try:
    response1 = opener1.open('https://www.httpbin.org/get')
    print(response1.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

# 需要认证的代理服务
proxy2 = 'username:password@127.0.0.1:7890'  # 加入认证信息
proxy_handler2 = ProxyHandler({
    'http': 'http://' + proxy2,
    'https': 'https://' + proxy2
})
opener2 = build_opener(proxy_handler2)
try:
    response2 = opener2.open('https://www.httpbin.org/get')
    print(response2.read().docode('utf-8'))
except URLError as e:
    print(e.reason)

# SOCKS类型代理
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
socket.socket = socks.socksocket
try:
    response3 = request.urlopen('https://www.httpbin.org/bget')
    print(response3.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

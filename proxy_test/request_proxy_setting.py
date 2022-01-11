# request的代理设置
import requests
import socket
import socks

# 普通模式
proxy = '127.0.0.1:7890'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}
try:
    response = requests.get('https://www.httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

# 认证模式
proxy1 = 'username:password@127.0.0.1:7890'
proxies1 = {
    'http': 'http://' + proxy1,
    'https': 'https://' + proxy1
}
try:
    response1 = requests.get('https://www.httpbin.org/get', proxies=proxies1)
    print(response1.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

# 设置SOCKS代理
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', '7891')
socket.socket = socks.socksocket
try:
    response2 = requests.get('https://www.httpbin.org/get')
    print(response2.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

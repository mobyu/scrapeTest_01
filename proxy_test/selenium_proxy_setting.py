# 为selenium设置代理
# 以Chrome浏览器为例
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

# 对于无认证代理可以如下设置
proxy = '127.0.0.1:7890'
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(options=options)
browser.get('https://www.httpbin.org/get')
print(browser.page_source)
browser.close()

# 对于需要认证的代理可以如下设计
ip = '127.0.0.1'
port = 7890
username = 'foo'
password = 'bar'

manifest_json = """"
{
  "version": "1.0.0",
  "manifest_version": 2,
  "name": "Chrome Proxy",
  "permissions": [
    "proxy",
    "tabs",
    "unlimitedStorage",
    "storage",
    "<all_urls>",
    "webRequest",
    "webRequestBlocking"
  ],
  "background": {
    "scripts": [
      "background.js"
    ]
  }
}
"""

background_js = """"
var config = {
  mode: "fixed_servers",
  rules: {
    singleProxy: {
      scheme: "http",
      host: "%(ip) s",
      port: "%(port) s"
    }
  }
}

chrome.proxy.setting.set({
  value: config,
  scope: "regular"
}, function() {});

function callbackFn(datails) {
  return {
    authCredentials: {
      username: "%(username) s"
      password: "%(password) s"
    }
  }
}

chrome.webRequest.onAuthRequired.addListener(
  callbackFn, {
    urls: ["<all_urls>"]
  }, ['blocking'])
""" % {'ip': ip, 'port': port, 'username': username, 'password': password}

# 本地创建 manifest.json配置文件和background.js脚本来设置认证代理。运行后会有一个proxy_auth_plugin.zip文件在本地生成
plugin_file = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(plugin_file, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
options = Options()
options.add_argument("--start-maximized")
options.add_extension(plugin_file)
browser = webdriver.Chrome(options=options)
browser.get('https://www.httpbin.org/get')
print(browser.page_source)
browser.close()

# 设置socks代理
proxy1 = '127.0.0.1:7891'
options1 = webdriver.ChromeOptions()
options1.add_argument('--proxy-server=socks5://' + proxy)  # 修改对应协议
browser1 = webdriver.Chrome(options=options1)
browser1.get('https://www.httpbin.org/get')
print(browser1.page_source)
browser.close()

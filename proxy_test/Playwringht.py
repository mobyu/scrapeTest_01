# 为Playwright
from playwright.sync_api import sync_playwright

# http协议
with sync_playwright() as p:
    browser = p.chromium.launch(proxy={
        'server': 'http://127.0.0.1:7890'
    })
    page = browser.new_page()
    page.goto('https://www.httpbin.org/get')
    print(page.content())
    browser.close()

# SOCKS协议，设置方法完全一样只是将协议换为socks5
'''
    browser = p.chromium.launch(proxy={
        'server': 'http://127.0.0.1:7890'
    })
'''

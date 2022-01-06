from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re


def parse_name(name_html):
    has_whole = name_html('.whole')  # 提取h3阶段class的名称赋给变量has_whole进行判断
    if has_whole:
        return name_html.text()
    else:
        chars = name_html('.char')  # 首先选取.char节点赋值给chars
        items = []
        for char in chars.items():  # 遍历chars变量，每次遍历对应一个span节点，提取节点text内容，作为字典text属性；提取style内容作为字典left属性
            items.append({
                'text': char.text().strip(),
                'left': int(re.search('(\d+)px', char.attr('style')).group(1))
            })
        # 调用sorted方法排序，两个参数：key（使用lambda表达式提取left属性）；reverse=False，表示从小到大排序
        items = sorted(items, key=lambda x: x['left'], reverse=False)

        return ''.join([item.get('text') for item in items])


browser = webdriver.Chrome()
browser.get('https://antispider3.scrape.center/')

WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.item')))
html = browser.page_source
doc = pq(html)
names = doc('.item .name')
for name_html in names.items():
    name = parse_name(name_html)
    print(name)
browser.close()

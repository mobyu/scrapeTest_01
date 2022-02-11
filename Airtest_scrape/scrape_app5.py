# -*- encoding=utf8 -*-
__author__ = "17253"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from loguru import logger
import os
import json

auto_setup(__file__)

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
window_width, window_height = poco.get_screen_size()
PACKAGE_NAME = 'com.goldze.mvvmhabit'
TOTAL_NUMBER = 100
OUTPUT_FOLDER = 'movie'
os.path.exists(OUTPUT_FOLDER) or os.makedirs(OUTPUT_FOLDER)
scrape_titles = []

# poco("com.sec.android.app.launcher:id/home_icon")

def scrape_index():
    elements = poco(f'{PACKAGE_NAME}:id/item')
    elements.wait_for_appearance()
    return elements


def scrape_detail(element):
    element.click()
    panel = poco(f'{PACKAGE_NAME}:id/content')
    panel.wait_for_appearance(5)
    title = poco(f'{PACKAGE_NAME}:id/title').attr('text')
    categories = poco(f'{PACKAGE_NAME}:id/categories_value').attr('text')
    socre = poco(f'{PACKAGE_NAME}:id/score_value').attr('text')
    published_at = poco(f'{PACKAGE_NAME}:id/published_at_value').attr('text')
    drama = poco(f'{PACKAGE_NAME}:id/drama_value').attr('text')
    keyevent('BACK')
    return {
        'title': title,
        'categories': categories,
        'socre': socre,
        'published_at': published_at,
        'drama': drama
    }


def scroll_up():
    swipe((window_width * 0.5, window_height * 0.8),
          vector=[0, -0.5], duration=1)


def save_data(element_data):
    with open(f'{OUTPUT_FOLDER}/{element_data.get("title")}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(element_data, ensure_ascii=False, indent=2))
        logger.debug(f'saved as fie {element_data.get("title")}.json')


def main():
    while len(scrape_titles) < TOTAL_NUMBER:
        elements = scrape_index()
        for element in elements:
            element_title = element.offspring(f'{PACKAGE_NAME}:id/tv_title')
            if not element_title.exists():
                continue
            title = element_title.attr('text')
            logger.debug(f'get title {title}')
            if title in scrape_titles:
                continue
            _, element_y = element.get_position()
            if element_y > 0.7:
                scroll_up()
            element_data = scrape_detail(element)
            save_data(element_data)
            scrape_titles.append(title)


if __name__ == '__main__':
    init_device("Android")
    stop_app(PACKAGE_NAME)
    start_app(PACKAGE_NAME)
    main()

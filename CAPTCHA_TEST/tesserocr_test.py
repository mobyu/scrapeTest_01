# 使用pytesseract包进行验证码识别

from PIL import Image
import pytesseract.pytesseract
import time
import re
from selenium import webdriver
from io import BytesIO
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np
import cv2
import ddddocr

# text = pytesseract.image_to_string(Image.open('E:\\Mydata\\picture\\code002.png'))
# print(text)

def captcha_value(image):
    det = ddddocr.DdddOcr(det=True)
    poses = det.detection(image)
    return poses


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    browser.get('https://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))
    captcha = captcha_value(image)
    # captcha = re.sub('[^A-Za-z0-9]]', '', captcha)
    # print(captcha)
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type="text"]').send_keys(captcha)
    browser.find_element(By.CSS_SELECTOR, '.login').click()
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//h2[contains(.,"登录成功")]')))
        time.sleep(10)
        browser.close()
        return True
    except TimeoutException:
        return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()

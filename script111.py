import time
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.baidu.com/
    page.goto("https://www.baidu.com/")

    # Click input[name="wd"]
    page.click("input[name=\"wd\"]")

    # Fill input[name="wd"]
    page.fill("input[name=\"wd\"]", "阿飞小可爱")

    # Press Enter
    # with page.expect_navigation(url="https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E9%98%BF%E9%A3%9E%E5%B0%8F%E5%8F%AF%E7%88%B1&fenlei=256&rsv_pq=c70eff72000f44c4&rsv_t=140dJJeIoIEGSY2Pd3ANrlglFLZjIxBa45iqWJz%2BJWv0zkGwQpQiePeu9Jc&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=30&rsv_sug1=27&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&prefixsug=%25E9%2598%25BF%25E9%25A3%259E%25E5%25B0%258F%25E5%258F%25AF%25E7%2588%25B1&rsp=5&inputT=14352&rsv_sug4=15988"):
    with page.expect_navigation():
        page.press("input[name=\"wd\"]", "Enter")

    # ---------------------
    time.sleep(5)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

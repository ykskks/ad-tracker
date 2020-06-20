import argparse
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# import chromedriver_binary


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="facebook ad page id")
    # parser.add_argument("--retrieve_all", action="store_true", help="retrieve all ads for the specified id")
    args = parser.parse_args()
    return args


def get_driver():
    options = Options()
    options.add_argument('--headless')  # GUIが開かない
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage')        
    # options.language = "JP"
    driver = webdriver.Chrome('/opt/chrome/chromedriver', options=options)
    return driver


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 5

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def retrieve_ad_info(driver, id_):
    url = "https://www.facebook.com/ads/library/" \
          "?active_status=all&ad_type=all&country=JP" \
          "&impression_search_field=has_impressions_lifetime&view_all_page_id=" \
          + id_
    CLASS_NAME_DIV = "_7owt"
    CLASS_NAME_STATUS = "_7jw1"
    CLASS_NAME_DATE = "_7jwu"
    CLASS_NAME_ID = "_4rhp"

    driver.get(url)
    scroll_to_bottom(driver)
    # 各広告のdivを取得
    elements = driver.find_elements(By.CLASS_NAME, CLASS_NAME_DIV)
    # 各divの中の基本情報を取得
    ad_infos = []
    for element in elements:
        ad_info = {}
        ad_info["status"] = element.find_element(By.CLASS_NAME, CLASS_NAME_STATUS).text
        ad_info["date"] = element.find_element(By.CLASS_NAME, CLASS_NAME_DATE).text
        ad_info["id"] = element.find_element(By.CLASS_NAME, CLASS_NAME_ID).text
        ad_infos.append(ad_info)
    print(ad_infos)
    print(len(ad_infos))


def main():
    args = get_arguments()
    id_ = args.id
    # retrieve_all = args.retrieve_all
    driver = get_driver()
    retrieve_ad_info(driver, id_)


if __name__ == "__main__":
    main()

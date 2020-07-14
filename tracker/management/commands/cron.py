import argparse
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# import chromedriver_binary
from django.core.management.base import BaseCommand

from ...models import Ad, Advertiser


class Command(BaseCommand):
    """
    現在登録さてれるAdvertiserのidを全て取得して
    それぞれに対してスクレイピングしてAdを取得し
    新しいものをDBに保存
    """
    def __init__(self):
        super().__init__()

        # TODO: 全部取得はデータ増えた時に大丈夫なのか？
        self.advertisers = Advertiser.objects.all()
        self.ads = Ad.objects.all()
        self.advertiser_ids = [advertiser.id for advertiser in self.advertisers]
        self.ad_ids = [ad.id for ad in self.ads]

    def handle(self, *args, **options):
        driver = get_driver()
        for id_ in self.advertiser_ids:
            ad_infos = retrieve_ad_info(driver, id_)
            self._check_and_register(id_, ad_infos)

    def _check_and_register(self, advertiser_id, ad_infos):
        """
        各advertiser_idに対して取得された全てのadについて
        ad_idが既に登録済みであるか確認し、登録済みでなければDBに登録する
        """
        for ad_info in ad_infos:
            if ad_info["id"] not in self.ad_ids:
                Ad.objects.create(
                    id=ad_info["id"],
                    is_active=True if ad_info["status"] == "Active" else False,
                    start_date=self._convert_date_format(ad_info["date"]),
                    advertiser=Advertiser.objects.get(id=advertiser_id)
                )

    def _convert_date_format(self, raw_date):
        month_map = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }
        month_day, year = raw_date.split(",")
        year = year.strip()
        month, day = month_day.split()
        date_in_format = f"{year}-{month_map[month]}-{day.zfill(2)}"
        return date_in_format


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
    CLASS_NAME_DIV = "_8k--"
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
        ad_info["date"] = element.find_element(By.CLASS_NAME, CLASS_NAME_DATE).find_element(By.TAG_NAME, "span").text
        ad_info["id"] = element.find_element(By.CLASS_NAME, CLASS_NAME_ID).text
        ad_infos.append(ad_info)
    return ad_infos


def main():
    args = get_arguments()
    id_ = args.id
    # retrieve_all = args.retrieve_all
    driver = get_driver()
    ad_infos = retrieve_ad_info(driver, id_)
    print(f"Retrieved {len(ad_infos)} ad_infos for id {id_}")


if __name__ == '__main__':
    main()

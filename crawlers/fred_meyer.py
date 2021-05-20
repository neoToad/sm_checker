from Crawler import Crawler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from test_soup import download_image

class FMCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.fredmeyer.com/search?query=squishmallow&searchType=suggestions&fulfillment=all",
                             local_ss='fred_m.xlsx')

    def run(self):
        items = self.driver.find_elements_by_class_name('kds-Image-img')
        for x in items:
            self.wanted_items.append(x.text)

        self.out_of_stock()
        self.add_new_items('ProductImages-image', "Claire's")

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change

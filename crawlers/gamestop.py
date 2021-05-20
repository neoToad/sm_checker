from Crawler import Crawler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from test_soup import download_image
import re


class GSCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.gamestop.com/search/?q=squishmallow&lang=default",
                         local_ss='gamestop.xlsx')
        self.item_names = []

    def add_new_items(self, class_name, site_name):
        spreadsheet_items = []
        for row_num in range(2, self.ws.max_row + 1):
            spreadsheet_items.append(self.ws.cell(row=row_num, column=1).value)

        for item in self.wanted_items:
            item.click()
            item_name = self.driver.find_element_by_class_name("product-name").text
            if item_name not in spreadsheet_items:
                image = self.driver.find_element_by_class_name(class_name)
                image_name = download_image(image.get_attribute("src"))
                self.update_row(item_name.text, 'None', 'Yes', image_name, 'to_upload', site_name)
                self.driver.back()
                self.change = True
            else:
                print(f"{item_name} already known")

    def check_for_series(self, spreadsheet_items):
        series_still_available = [series for series in self.item_names]
        print(series_still_available)
        out_of_stock_series = self.diff(series_still_available, spreadsheet_items)

        self.delete_oos_series(out_of_stock_series)

    def run(self):
        items_area = self.driver.find_element_by_class_name('product-tiles-row')
        items = items_area.find_elements_by_class_name("product-tile")
        for x in items:
            in_store_only = re.search(r'In Store only', x.text)
            if in_store_only:
                print("in store only")
            else:
                self.item_names.append(x.find_element_by_class_name("link-name").text)
                self.wanted_items.append(x)

        self.out_of_stock()
        self.add_new_items('zoomImg', 'GameStop')

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change

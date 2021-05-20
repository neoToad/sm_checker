from Crawler import Crawler
import selenium


class WalmartCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.walmart.com/search/search-ng.do?search_query=squishmallow",
                         local_ss='walmart.xlsx')
        self.another_page = True

    def click_next_page(self):
        if self.driver.find_element_by_class_name('paginator-btn-next'):
            next_btn = self.driver.find_element_by_class_name('paginator-btn-next')
            next_btn.click()
        else:
            self.another_page = False

    def run(self):
        items = self.driver.find_elements_by_class_name('product-title-link')
        for x in items:
            self.wanted_items.append(x.text)

        self.out_of_stock()

        while self.another_page:
            try:
                self.add_new_items('hover-zoom-hero-image', "Walmart")
                self.click_next_page()
            except selenium.common.exceptions.TimeoutException:
                print("timeout exception")
                break

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change

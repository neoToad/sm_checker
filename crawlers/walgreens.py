from Crawler import Crawler
import re


class WalgreensCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.walgreens.com/search/results.jsp?Ntt=squishmallows",
                             local_ss='walgreens.xlsx')

    def run(self):
        items = self.driver.find_elements_by_class_name('product__details')
        for x in items:
            name = x.text.split('\n')[1]
            in_store_only = re.search(r'Not available for shipping', x.text)
            no_shipping = re.search(r'Out of stock for shipping', x.text)
            if in_store_only or no_shipping:
                print("no shipping")
            else:
                self.wanted_items.append(name)

        self.out_of_stock()
        self.add_new_items('productimage', "Walgreen's")

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change


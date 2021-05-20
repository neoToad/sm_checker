from Crawler import Crawler
import re


class TargetCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.target.com/s?searchTerm=squishmallow&facetedValue=5zktx&Nao=0",
                             local_ss='target.xlsx')

    def run(self):
        print("starting")
        items = self.driver.find_elements_by_class_name('styles__StyledDetailsWrapper-mkgs8k-6')
        for x in items:
            name = x.text.split('\n')[0]
            no_shipping = re.search(r'Shipping not available', x.text)
            if no_shipping:
                print("no shipping")
            else:
                self.wanted_items.append(name)

        self.out_of_stock()
        self.add_new_items('WRnFU', "Target")

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change


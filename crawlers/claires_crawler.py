from Crawler import Crawler


class ClairsCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.claires.com/us/toys-and-collectibles/plush-toys/?prefn1=brandName&prefv1"
                             "=Squishmallows",
                             local_ss='claires.xlsx')

    def run(self):
        items = self.driver.find_elements_by_class_name('product-name')
        for x in items:
            self.wanted_items.append(x.text)

        self.out_of_stock()
        self.add_new_items('primary-image', "Claire's")

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change





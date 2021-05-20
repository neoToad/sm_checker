from Crawler import Crawler
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from test_soup import download_image


class CostcoCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.costco.com/CatalogSearch?dept=All&keyword=squishmallows",
                             local_ss='costco.xlsx')

    def add_new_items(self, class_name, alt_class_name=None):
        spreadsheet_items = []
        for row_num in range(2, self.ws.max_row + 1):
            spreadsheet_items.append(self.ws.cell(row=row_num, column=1).value)

        for item in self.wanted_items:
            if item not in spreadsheet_items:
                to_click = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, item)))
                print(item)
                print(to_click.text)
                # time.sleep(2)
                to_click.click()

                dif_styles = self.driver.find_elements_by_xpath("//span[@class='selection-item']")

                if dif_styles:
                    for style in dif_styles:
                        style.click()
                        image_wrapper = self.driver.find_element_by_class_name(class_name)
                        image = image_wrapper.find_element_by_tag_name('img')
                        image_name = download_image(image.get_attribute("src"), '&id=', '&recipeID=')
                        self.update_row(item, style.text, 'Yes', image_name, 'to_upload', 'Costco')
                    self.change = True
                    self.driver.back()
                else:
                    price = self.driver.find_element_by_class_name('value').text
                    image_ = self.driver.find_element_by_id("RICHFXViewerContainer___richfx_id_0_zoomImage")
                    image_name2 = download_image(image_.get_attribute("src"), '&id=', '&recipeId=')
                    self.update_row(item, 'None', 'Yes', image_name2, 'to_upload', 'Costco', price)
                    self.change = True
                    self.driver.back()

    def run(self):
        items = self.driver.find_elements_by_class_name('description')
        for x in items:
            self.wanted_items.append(x.text)

        self.out_of_stock()
        self.add_new_items('RICHFXColorChange')

        self.wb.save(self.spread_filepath)
        self.wb.close()
        self.wb2.save(self.update_ss)
        self.wb2.close()

        self.driver.close()
        return self.change



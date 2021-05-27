from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import selenium
from sm_checker.Crawler import Crawler
from sm_checker.test_soup import find_styles, get_image, download_image
from sm_checker.xl_helpx import move_to_
import time
import logging

logging.basicConfig(filename="crawler_log.txt", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)



class ClairsCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.claires.com/us/toys-and-collectibles/plush-toys/?prefn1=brandName&prefv1"
                         "=Squishmallows",
                         local_ss='claires.xlsx', listing_class_name='product-name')

    def get_short_name(self, full_name):
        try:
            name = full_name.split('™ ')[-1].split('-')[0]
            if name[0].isdigit():   # Cuts out the size at beginning of name.
                if name[1].isdigit():
                    return name[4:]    # For sizes 10 and above
                return name[3:]
            else:
                return name
        except AttributeError:
            return ' '

    def get_price(self, price_name):
        text_e = self.driver.find_elements_by_xpath("//span[@class='price-sales']")
        return text_e[-1].text.split()[-1]

    def check_price_found(self, price_found, price_element):
        if price_found:
            return price_element.get_attribute(price_found)
        else:
            return price_element[1:]

    def run(self):
        self.load_items_from_site(self.listing_class_name)

        self.out_of_stock()
        self.add_new_items('primary-image', "Claire's", "price-sales")

        self.close_workbooks()

        self.driver.close()
        return self.change


class CostcoCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.costco.com/CatalogSearch?dept=All&keyword=squishmallows",
                             local_ss='costco.xlsx', listing_class_name='description')

    def add_new_items(self, class_name):
        spreadsheet_items = self.load_spread_data()

        for item in self.wanted_items:
            if item == "Hotstar Annual Subscription + 1 Bonus Month eGift Card":
                continue
            if item not in spreadsheet_items:
                to_click = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, item)))
                to_click.click()

                dif_styles = self.driver.find_elements_by_xpath("//span[@class='selection-item']")

                if dif_styles:
                    for style in dif_styles:
                        style.click()
                        image_wrapper = self.driver.find_element_by_class_name(class_name)
                        image = image_wrapper.find_element_by_tag_name('img')
                        price_e = self.driver.find_element_by_class_name('value')
                        image_name = download_image(image.get_attribute("src"), '&id=', '&re', rd=True)
                        self.update_row(item, style.text, 'Yes', image_name, 'to_upload', 'Costco', price_e.text)
                    self.change = True
                    self.driver.back()
                else:
                    price = self.driver.find_element_by_class_name('value').text
                    image_ = self.driver.find_element_by_id("RICHFXViewerContainer___richfx_id_0_zoomImage")
                    image_name2 = download_image(image_.get_attribute("src"), '&id=', '&recipeId=')
                    self.update_row(item, 'None', 'Yes', image_name2, 'to_upload', 'Costco', price)
                    self.change = True
                    self.driver.back()

    def get_short_name(self, full_name):
        try:
            name = full_name.split('"')[-1]
            if str(name.strip()) == 'Plush':
                new_name = "Squishmallow"
                return str(new_name.strip())
            else:
                return full_name.split('"')[-1].split('Plush')[0]

        except AttributeError:
            return ' '

    def run(self):
        self.load_items_from_site(self.listing_class_name)

        self.out_of_stock()
        try:
            self.add_new_items('RICHFXColorChange')
        except selenium.common.exceptions.NoSuchElementException:
            print("Error")
            pass

        self.close_workbooks()

        self.driver.close()
        return self.change


class GSCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.gamestop.com/search/?q=squishmallow&lang=default",
                         local_ss='gamestop.xlsx', listing_class_name=None)
        self.item_names = []

    def get_size(self, full_name):
        return 'N/A'

    def add_new_items(self, class_name, site_name):
        spreadsheet_items = self.load_spread_data()

        for item in self.wanted_items:
            item_idx = self.wanted_items.index(item)
            item_name = self.item_names[item_idx]
            item_listing = item.text
            item.click()
            print(item_name, " hello")
            print(item_listing)
            if item_name not in spreadsheet_items:
                self.find_image_and_price(item_name, class_name, site_name, item_listing, price_found=None)
            else:
                print(f"{item_name} already known")

    def load_spread_data(self):
        spreadsheet_items = []
        for row_num in range(2, self.ws.max_row + 1):
            spreadsheet_items.append(self.ws.cell(row=row_num, column=1).value.strip('\n'))
        return spreadsheet_items

    def check_price_found(self, price_found, price_element):
        if price_found:
            return price_element.get_attribute(price_found)
        else:
            return price_element

    def get_price(self, price_name):
        return price_name.split('$')[-1]

    def get_short_name(self, full_name):
        try:
            return full_name.split('Squishmallow')[-1].split('Only')[0]
        except AttributeError:
            return ' '


    def get_image(self, class_name):
        return self.driver.find_element_by_class_name(class_name)

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

        self.close_workbooks()

        self.driver.close()
        return self.change


class TargetCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.target.com/s?searchTerm=squishmallow&facetedValue=5zktx&Nao=0",
                             local_ss='target.xlsx', listing_class_name='styles__StyledDetailsWrapper-mkgs8k-6')

    def check_price_found(self, price_found, price_element):
        if price_found:
            return price_element.get_attribute(price_found)
        else:
            print(price_element.text)
            return price_element.text[1:]

    def run(self):
        print("starting")
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                                                   self.listing_class_name)))
        items = self.driver.find_elements_by_class_name('styles__StyledDetailsWrapper-mkgs8k-6')
        for x in items:
            name = x.text.split('\n')[0]
            shipping = x.text.split('\n')[5]
            print(name, shipping)
            no_shipping = re.search(r'Shipping not available', shipping)
            if no_shipping:
                print("no shipping")
            else:
                self.wanted_items.append(name)
                print(self.wanted_items)

        self.out_of_stock()
        self.add_new_items('styles__ThumbnailImage-beej2j-11', "Target", 'style__PriceFontSize-sc-17wlxvr-0')

        self.close_workbooks()

        self.driver.close()
        return self.change


class WalgreensCrawler(Crawler):
    def __init__(self):
            super().__init__(site_to_check=
                             "https://www.walgreens.com/search/results.jsp?Ntt=squishmallows",
                             local_ss='walgreens.xlsx', listing_class_name='product__details')

    def get_short_name(self, full_name, style):
        return full_name.text.split('\n')[1]

    def run(self):
        items = self.driver.find_elements_by_class_name('product__details')
        for x in items:
            in_store_only = re.search(r'Not available for shipping', x.text)
            no_shipping = re.search(r'Out of stock for shipping', x.text)
            if in_store_only or no_shipping:
                print("no shipping")
            else:
                self.wanted_items.append(x.text)

        self.out_of_stock()
        self.add_new_items('productimage', "Walgreen's", "product__price")

        self.close_workbooks()

        self.driver.close()
        return self.change


class WalmartCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.walmart.com/search/search-ng.do?search_query=squishmallow",
                         local_ss='walmart.xlsx', listing_class_name='product-title-link')
        self.another_page = True

    def click_next_page(self):
        if self.driver.find_element_by_class_name('paginator-btn-next'):
            next_btn = self.driver.find_element_by_class_name('paginator-btn-next')
            next_btn.click()
        else:
            self.another_page = False

    def check_price_found(self, price_found, price_element):
        print(price_element.text[1:])
        return price_element.text[1:]

    def run(self):
        items = self.driver.find_elements_by_class_name('product-title-link')
        for x in items:
            self.wanted_items.append(x.text)

        self.out_of_stock()

        while self.another_page:
            try:
                self.add_new_items('hover-zoom-hero-image', "Walmart", 'price-group')
                self.click_next_page()
            except:
                logging.exception('Walmart error!')
                break

        self.close_workbooks()

        self.driver.close()
        return self.change


class FiveBelowCrawler(Crawler):

    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.fivebelow.com/",
                         local_ss='fb_sm.xlsx', listing_class_name=None)

    def goto_stuffed_a(self):
        # open toys hover menu in top nav bar
        toys_menu = self.driver.find_element_by_link_text("toys & games")
        self.actions.move_to_element(toys_menu).perform()
        self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "stuffed animals"))).click()

    def load_products(self):
        all_products_loading = True
        while all_products_loading:
            try:
                self.driver.find_element_by_id("loadMoreProducts").click()
            except selenium.common.exceptions.ElementNotInteractableException:
                all_products_loading = False

    def check_series_out_of_stock(self):
        # Check if item in spreadsheet but not on website
        spreadsheet_items = self.load_spread_data()

        self.check_for_series(spreadsheet_items)

    def known(self, item, style, in_stock):
        # Return true if website is current with spreadsheet.
        for row_num in range(2, self.ws.max_row + 1):
            item_series_name = self.ws.cell(row=row_num, column=1).value
            item_style = self.ws.cell(row=row_num, column=2).value
            item_instock = self.ws.cell(row=row_num, column=3).value
            if item_series_name == item and item_style == style and in_stock == item_instock:
                return True

    def check_for_items(self):
        for item in self.wanted_items:
            item.click()
            time.sleep(2)
            dif_styles = find_styles(self.driver.current_url)
            self.check_for_styles(dif_styles, item)

            self.driver.back()

    def check_for_styles(self, dif_styles, item):
        if dif_styles == False:  # If one style, check if known in spreadsheet and if not add it
            if not self.known(item.text, 'single', 'Yes'):
                price_e = self.get_price('c01229')
                price = price_e.text.split(':')[-1]
                price = price[1:]
                logging.info(f'{price_e.text} / {price}')
                self.image_file = get_image(self.driver.current_url, None, 'image-gallery-slide center')
                self.update_row(item.text, 'single', 'Yes', self.image_file, 'to_upload', 'Five Below', price)
                self.change = True
        else:
            self.check_each_style(dif_styles, item)

    def get_price(self, price_name):
        return self.driver.find_element_by_xpath('//span[@data-cy="cartDropdown__itemPrice"]')

    def check_each_style(self, styles, item):
        for style in styles:
            style_name_tag = self.driver.find_element_by_xpath(f"//*[name()='svg']/*[text()='{style}']")
            parent_tag = style_name_tag.find_element_by_xpath("./..")
            parent_tag.click()
            parent_cls_attr = parent_tag.get_attribute('class')
            parent_cls_attrs = parent_cls_attr.split()
            print(parent_cls_attrs)
            if 'active' in parent_cls_attr.split():
                print('Button active')
                if not self.known(item.text, style, 'Yes'):
                    self.image_file = get_image(self.driver.current_url, styles.index(style), 'image-gallery-slide '
                                                                                              'center')
                    price_e = self.get_price('c01229')
                    price = price_e.text.split(':')[-1]
                    price = price[1:]
                    self.update_row(item.text, style, 'Yes', self.image_file, 'to_upload', 'Five Below', price)
                    self.change = True
                    print(f'{style} button is enabled')
            else:
                if not self.known(item.text, style, 'No'):
                    self.update_row(item.text, style, 'No', None, 'to_delete', ' ', ' ')
                    self.change = True
                    print(f'{style} button is NOT enabled')

    def get_short_name(self, full_name, style):
        return style

    def get_size(self, full_name):
        regexp = re.compile(r'in')
        for x in full_name.split():
            if regexp.search(x):
                if x == 'Rainbow':
                    continue
                else:
                    return x
        return 'N/A'

    def run_crawler(self):
        self.driver.get(self.site_to_check)
        self.driver.maximize_window()
        self.driver.find_element_by_tag_name('button').click()

        # wait = WebDriverWait(self.driver, 10)
        # actions = ActionChains(self.driver)
        try:
            self.goto_stuffed_a()
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(2)
            self.goto_stuffed_a()

        time.sleep(2)
        self.load_products()

        ## Find items with name

        self.wanted_items = self.driver.find_elements_by_partial_link_text("squishmallows")
        self.newRowLocation = self.ws.max_row + 1

        self.out_of_stock()
        self.check_for_items()

        self.close_workbooks()
        self.driver.quit()
        return self.change


class PaperStoreCrawler(Crawler):
    def __init__(self):
        super().__init__(site_to_check=
                         "https://www.thepaperstore.com/c/squishmallows",
                         local_ss='paper_store.xlsx', listing_class_name='listing__name')

    def get_image(self, class_name):
        image_wrap = WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
        return image_wrap.find_element_by_tag_name('img')

    def get_short_name(self, full_name):
        try:
            return full_name.split('Squishmallows')[-1].split('(')[0]
        except AttributeError:
            return ' '

    def get_size(self, full_name):
        return full_name[full_name.find("(")+1:full_name.find(")")]

    def run(self):
        self.load_items_from_site(self.listing_class_name)

        # check if an item is now out of stock
        self.out_of_stock()

        self.add_new_items("product-images--image-wrap", 'The Paper Store', "product-information--purchase_price", 'data-base-price')

        self.close_workbooks()

        self.driver.close()

        return self.change


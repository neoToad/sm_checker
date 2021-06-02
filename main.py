from crawlers.crawlers import CostcoCrawler, GSCrawler, TargetCrawler, WalgreensCrawler, WalmartCrawler, ClairsCrawler, \
    FiveBelowCrawler, PaperStoreCrawler
from update_trigger import update_site_live, upload_images
import logging
from xl_helpx import delete_updated_items_ss
import time

logging.basicConfig(filename="crawler_log.txt", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    while True:
        checked_sites = []
        try:
            five_below_crawler = FiveBelowCrawler().run_crawler()
            checked_sites.append(five_below_crawler)
        except:
            logging.exception('\n\nFive Below error!')

        try:
            paper_store = PaperStoreCrawler().run()
            checked_sites.append(paper_store)
        except:
            logging.exception('\n\nPaper Store Error error!')

        try:
            claires = ClairsCrawler().run()
            checked_sites.append(claires)
        except:
            logging.exception('\n\nClaires Error error!')
        #
        try:
            costco = CostcoCrawler().run()
            checked_sites.append(costco)
        except:
            logging.exception('\n\nCostco Error error!')

        try:
            game_stop = GSCrawler().run()
            checked_sites.append(game_stop)
        except:
            logging.exception('\n\nGame Stop Error!')

        try:
            walmart = WalmartCrawler().run()
            checked_sites.append(walmart)
        except:
            logging.exception('\n\nWalmart Error!')

        try:
            walgreens = WalgreensCrawler().run()
            checked_sites.append(walgreens)
        except:
            logging.exception('\n\nWalgreens Error!')

        try:
            target = TargetCrawler().run()
            checked_sites.append(target)
        except:
            logging.exception('\n\nTarget Error!')

        if True in checked_sites:
            update_site_live()
            delete_updated_items_ss()
            time.sleep(10)
            upload_images()
            print('waiting')
            time.sleep(3600)
            print('running')

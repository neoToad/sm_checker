from crawlers.crawlers import CostcoCrawler, GSCrawler, TargetCrawler, WalgreensCrawler, WalmartCrawler, ClairsCrawler, FiveBelowCrawler, PaperStoreCrawler
from update_trigger import update_site_live, upload_images
import logging
from xl_helpx import delete_updated_items_ss

logging.basicConfig(filename="crawler_log.txt", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    checked_sites = []

    try:
        five_below_crawler = FiveBelowCrawler().run_crawler()
        checked_sites.append(five_below_crawler)
    except:
        logging.exception('Five Below error!')

    try:
        paper_store = PaperStoreCrawler().run()
        checked_sites.append(paper_store)
    except:
        logging.exception('Paper Store Error error!')

    try:
        claires = ClairsCrawler().run()
        checked_sites.append(claires)
    except:
        logging.exception('Claires Error error!')

    try:
        costco = CostcoCrawler().run()
        checked_sites.append(costco)
    except:
        logging.exception('Costco Error error!')

    # game_stop = GSCrawler().run()
    # walmart = WalmartCrawler().run()
    # walgreens = WalgreensCrawler().run()
    # target = TargetCrawler().run()

    if True in checked_sites:
        update_site_live()
        upload_images()
        delete_updated_items_ss()




from crawlers.claires_crawler import ClairsCrawler
from crawlers.five_below_crawler import FiveBelowCrawler
from crawlers.costco import CostcoCrawler
from crawlers.gamestop import GSCrawler
from crawlers.paper_store_c import PaperStoreCrawler
from crawlers.walmart import WalmartCrawler
from crawlers.walgreens import WalgreensCrawler
from crawlers.target import TargetCrawler

from update_trigger import update_site


if __name__ == "__main__":

    five_below_crawler = FiveBelowCrawler().run_crawler()
    paper_store = PaperStoreCrawler().run()
    claires = ClairsCrawler().run()
    costco = CostcoCrawler().run()
    #
    # # # TODO fred meyer
    # # # fm = FMCrawler().run()
    #
    game_stop = GSCrawler().run()
    walmart = WalmartCrawler().run()
    walgreens = WalgreensCrawler().run()
    target = TargetCrawler().run()

    if walmart:
        update_site()



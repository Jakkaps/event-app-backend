import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time
import argparse

#Import all spiders
from spiders import abakus_spider, samfundet_spider, facebook_spider

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()

    if not args.debug:
        time.sleep(30)

    while True:
        process = CrawlerProcess(get_project_settings())
        # process.crawl(abakus_spider.AbakusSpider)
        # process.crawl(samfundet_spider.SamfundetSpider)
        process.crawl(facebook_spider.FacebookSpider)
        
        process.start()

        time.sleep(3600)


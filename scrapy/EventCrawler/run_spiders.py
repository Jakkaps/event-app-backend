import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import time


#Import all spiders
from spiders import abakus_spider
from spiders import samfundet_spider

if __name__ == "__main__":

    while True: 
        process = CrawlerProcess(get_project_settings())
        process.crawl(abakus_spider.AbakusSpider)
        process.crawl(samfundet_spider.SamfundetSpider)
        process.start()

        time.sleep(3600)


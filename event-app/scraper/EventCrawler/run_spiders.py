import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import time
import os
import argparse

#Import all spiders
from scraper.EventCrawler.spiders import abakus_spider, samfundet_spider, facebook_spider

def run_crawler(): 
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='project')
    
    process = CrawlerProcess(settings)
    process.crawl(abakus_spider.AbakusSpider)
    process.crawl(samfundet_spider.SamfundetSpider)
    process.crawl(facebook_spider.FacebookSpider)

    process.start()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()



    if not args.debug:
        time.sleep(30)
        while True:
            run_crawler()
            time.sleep(3600)

    else:
        run_crawler()


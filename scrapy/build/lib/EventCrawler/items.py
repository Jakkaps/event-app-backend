# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Event(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    host = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    study_program = scrapy.Field()
    class_year = scrapy.Field()
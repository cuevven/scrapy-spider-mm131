# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapymm131Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # gallery = scrapy.Field()
    # albums = scrapy.Field()
    album_name = scrapy.Field()
    album_URLs = scrapy.Field()
    referer = scrapy.Field()
    pass

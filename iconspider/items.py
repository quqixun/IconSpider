# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IconSpiderItem(scrapy.Item):
    # Indicate the url of an icon
    file_urls = scrapy.Field()

    # Indicate the file of an icon
    files = scrapy.Field()

    # NOTE: DO NOT CHANGE NAMES OF THESE VARIABLES

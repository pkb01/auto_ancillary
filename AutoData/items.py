# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AncillaryDetailsItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    MainPageUrl = Field()

    companyName = Field()
    industry = Field()
    companyType = Field()
    
    contactNumber = Field()
    city = Field()
    companyWebsite = Field()


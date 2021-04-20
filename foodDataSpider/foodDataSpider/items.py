# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FooddataspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
class LocalitiesItem(scrapy.Item):
    placeNames = scrapy.Field()
    links = scrapy.Field()
class ZomatoSpiderItem(scrapy.Item):
    restaurant_title = scrapy.Field()
    restaurant_rating = scrapy.Field()
    restaurant_tag = scrapy.Field()
    restaurant_cost_for_one = scrapy.Field()
    restaurant_min_price_and_time = scrapy.Field()
    restaurant_total_reviews = scrapy.Field()
    restaurant_payment_methods = scrapy.Field()

class ZomatoRestaurant(scrapy.Item):
    resid = scrapy.Field()
    name = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()
    imageUrl = scrapy.Field()



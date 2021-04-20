import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['amazon.com']
    start_urls = [
        'http://amazon.com/s/ref=lp '
    ]

    def parse(self, response):
        pass

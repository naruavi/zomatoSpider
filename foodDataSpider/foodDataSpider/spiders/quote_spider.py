import scrapy
from scrapy.http import FormRequest
from ..items import FooddataspiderItem


class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com'
    ]

    def parse(self, response, **kwargs):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(
                ".//span[@class='text']/text()").extract_first()
            author = quote.xpath(
                ".//small//text()"
            ).extract_first()
        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token':token,
            'username':'someone',
            'password':'something'
        }, callback = self.start_scraping)

    def start_scraping(self, response):
        items = FooddataspiderItem()

        all_div_quotes = response.css("div.quote")

        for quotes in all_div_quotes:
            title = quotes.css("span.text::text").extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items
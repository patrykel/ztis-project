import scrapy
from utils import clean

BASE_URL = 'http://www.bankier.pl'

class BankierScraper(scrapy.Spider):
    name = "Bankier"
    start_urls = [
        BASE_URL + '/waluty/wiadomosci'
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        for article in response.css('div.article'):
            yield {
                'date': article.css('time.entry-date::text').extract_first(),
                'title': clean(article.css('span.entry-title a::text').extract_first()),
                'content': clean(article.css('p::text').extract_first()),
            }

        next_page = response.css('a.next::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(BASE_URL + next_page, callback=self.parse)

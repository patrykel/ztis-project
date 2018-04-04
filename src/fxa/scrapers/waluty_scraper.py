import locale
import time
import scrapy
from utils import clean

WEBSITE_URL = "http://waluty.com.pl"
BASE_URL = "http://waluty.com.pl/section.php?id=30&mode=archive&page=%s"

def make_url(page):
    return BASE_URL % (page)

class WalutyScraper(scrapy.Spider):
    name = "Waluty.com"
    page = 1
    start_urls = [
        make_url(page)
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        articles = response.css('div.article')
        if not articles: return

        for article in response.css('div.article'):
            article_content_url = article.css('h3 a::attr("href")').extract_first()
            article_request = scrapy.Request(WEBSITE_URL + article_content_url, callback=self.parse_article_content)
            yield article_request

        self.page = self.page + 1
        yield scrapy.Request(make_url(self.page), callback=self.parse)



    def parse_article_content(self, response):
        date_string = clean(response.css('div.article span.date::text').extract_first())
        return {
            "date": self.parse_datetime(date_string),
            "title": clean(response.css('div.article h3 a::text').extract_first()),
            "content": clean(response.css('div.article div.tekst strong::text').extract_first())
        }

    def parse_datetime(self, date):
        locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
        time_struct = time.strptime(date, '%d.%m.%Y %H:%M %A')
        return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

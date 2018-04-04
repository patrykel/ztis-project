import locale
import time
import scrapy
from utils import clean


BASE_URL = 'http://biznes.onet.pl/_cdf/api?json={"params":{"offset":%s,"limit":15,"servicePaths":[{"name":"biznes.waluty.wiadomosci","priority":1}],"keys":["servicePaths","namespace"],"solrOldUrl":false,"serviceName":"Biznes","namespace":[{"name":"go","priority":1}],"isCanonical":"*","resolveRelated":1,"listUrl":"/waluty/wiadomosci","__sp":"biznes"}}&____presetName=liststream'

def make_url(offset):
    return BASE_URL % (offset)

class OnetScraper(scrapy.Spider):
    name = "Onet biznes"
    offset = 8999
    start_urls = [
        make_url(offset)
    ]
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_date(self, date):
        locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
        time_struct = time.strptime(date, '%d %b %y %H:%M')
        return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

    def parse(self, response):
        articles = response.css('div.itArticle').extract()
        if not articles: return

        for article in response.css('div.itArticle'):
            yield {
                'date': self.parse_date(clean(article.css('div.datePublished::text').extract_first())),
                'title': clean(article.css('h3.itemTitle::text').extract_first()),
                'content': clean(article.css('div.itemLead::text').extract_first()),
            }
        self.offset = self.offset + 15
        yield scrapy.Request(make_url(self.offset), callback=self.parse)

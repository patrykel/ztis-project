from newsapi import NewsApiClient
import scrapy
import datetime

newsapi = NewsApiClient(api_key='791699a09e634365b7edca7815029d6c')


def parse_date(date):
    parsed_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date()
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')


class NewsScraper(scrapy.Spider):
    all_articles = newsapi.get_everything(q='euro',
                                          language='en',
                                          sort_by='relevancy')

    for i in range(all_articles['totalResults'] / 20):
        partial_articles = newsapi.get_everything(q='euro',
                                                  language='en',
                                                  sort_by='relevancy',
                                                  page=i+1)

        # tutaj zmienić żeby dostosować do kodu, poniższe linie wypiszę wszystkie notki z zapytania wyżej w formacie
        # odpowiadającym plikowi rss_unique.csv w data/notes
        #for article in all_articles['articles']:
            #print("en_news_api" + " | " + parse_date(article['publishedAt']) + " | " + article['title'] + " | " + article['description'])
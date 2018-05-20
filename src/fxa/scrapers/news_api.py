from newsapi import NewsApiClient
import scrapy
import datetime
import csv


CURRENCY = 'euro'

# newsapi = NewsApiClient(api_key='791699a09e634365b7edca7815029d6c')
newsapi = NewsApiClient(api_key='81a67c69e5f64233b124075faec2bc96')


def parse_date(date):
    parsed_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").date()
    return parsed_date.strftime('%Y-%m-%d %H:%M:%S')


class NewsScraper(scrapy.Spider):
    myFile = open(CURRENCY + '.csv', 'a')
    writer = csv.writer(myFile)

    all_articles = newsapi.get_everything(q=CURRENCY,
                                          language='en')

    # print(all_articles['totalResults'])
    for i in range(499, int(all_articles['totalResults'] / 20)):
        print(i)
        partial_articles = newsapi.get_everything(q=CURRENCY,
                                                  language='en',
                                                  sort_by='publishedAt',
                                                  page=i+1)

        # tutaj zmienić żeby dostosować do kodu, poniższe linie wypiszę wszystkie notki z zapytania wyżej w formacie
        # odpowiadającym plikowi rss_unique.csv w data/notes
        for article in partial_articles['articles']:
            writer.writerows([["en_news_api", parse_date(article['publishedAt']), article['title'], article['description']]])
            #print("en_news_api" + " | " + parse_date(article['publishedAt']) + " | " + article['title'] + " | " + article['description'])

    myFile.close()
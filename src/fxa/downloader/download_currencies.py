from fxa.currencies.web_currencies_repository import *
import csv
import datetime



# date generator function
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def download_currency(base, currency, start_date_str, end_date_str, csv_filename):
    '''
    :param base:            base currency like USD (case insensitive)
    :param currency:        other currency like PLN (case insensitive)
    :param start_date_str:  string with start date (inclusive) in format YYYY-MM-DD like 2018-01-02
    :param end_date_str:    string with end date (exclusive) in format YYYY-MM-DD like 2018-12-31
    :param csv_filename:
    :return:
    '''
    base = base.upper()
    currency = currency.upper()
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    webCurrenciesRepository = WebCurrenciesRepository()

    with open(csv_filename, 'a') as csvfile:
        currency_writer = csv.writer(csvfile, delimiter=';')

        for single_date in daterange(start_date, end_date):
            print("Download currency {}-{} for date: {}".format(base, currency, single_date.strftime("%Y %m %d")))

            date = single_date.strftime("%Y%m%d %H%M%S")
            rate = webCurrenciesRepository.get_currency_rate(base, currency, single_date)
            volume = 0

            # write a row to csv
            '''
            date        # date like 20181231 235959
            open        # opening currency
            high        # highest currency in a day
            low         # lowest currency in a day
            close       # closing currency
            volume
            '''
            currency_writer.writerow([date] + [rate] * 4 + [volume])

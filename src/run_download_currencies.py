import argparse
from fxa.downloader.download_currencies import download_currency


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base',
                        action='store',
                        required=True,
                        help='Base currency name. E.g. USD')
    parser.add_argument('-c', '--currency',
                        action='store',
                        required=True,
                        help='Target currency name. E.g. PLN')
    parser.add_argument('-s', '--startdate',
                        action='store',
                        help='Start date (inclusive) in format YYYY-MM-DD like 2018-01-02')
    parser.add_argument('-e', '--enddate',
                        action='store',
                        help='End date (exclusive) in format YYYY-MM-DD like 2018-12-31')
    parser.add_argument('-f', '--filepath',
                        action='store',
                        help='Currencies CSV archive file path.')

    args = parser.parse_args()

    download_currency(
        args.base,
        args.currency,
        args.startdate,
        args.enddate,
        args.filepath
    )

if __name__ == '__main__':
    main()
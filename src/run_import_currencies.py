import argparse
from fxa.importer.import_currencies import import_currencies_single_csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base',
                        action='store',
                        required=True,
                        help='Base currency name. E.g. EUR')
    parser.add_argument('-c', '--currency',
                        action='store',
                        required=True,
                        help='Target currency name. E.g. PLN')
    parser.add_argument('filepath',
                        action='store',
                        help='Currencies archive file path.')
    args = parser.parse_args()

    import_currencies_single_csv(
        args.base,
        args.currency,
        args.filepath
    )

if __name__ == '__main__':
    main()

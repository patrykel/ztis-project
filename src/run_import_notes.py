import argparse
import fxa.importer.import_notes as importer
import code

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir',
                        action='store',
                        required=True,
                        help='Root directory with notes data.')

    parser.add_argument('-n', '--default_name',
                        action='store',
                        required=False,
                        default="rss_unique.csv",
                        help='Default name of file with data')

    args = parser.parse_args()
    importer.import_notes_directory(args.dir, args.default_name)

if __name__ == "__main__":
    main()

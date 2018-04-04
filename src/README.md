# ZTIS Foreign Currency Analyzer (FXA)

## DB Config
This project uses PostgreSQL as its database.
The assumed database config is:
```
user = postgres
password = postgres
db = ztis_fxa
host = localhost
port = 5432
```
This configuration can be changed in `fxa/config/db`

Additional scripts for DB related actions are located inside `sql` directory.

## Repository structure
This repository contains the following directories:

* `data` - Place all data (notes, currencies, doc2vec models, etc.) there. Note that this folder is excluded from source control to avoid commiting large files
* `docs` - Project documentation with Latex sources
* `fxa` - Main source directory:
    * `config` - Contains configuration files and DB connection
    * `currencies` - Contains currencies repositories and models
    * `dictionaries` - Contains dictionaries and dictionary providers
    * `importer` - Contains scripts for importing data into DB
    * `ml` - Contains Machine Learning related scripts
    * `notes` - Contains notes repositories and models
    * `preprocessing` - Contains preprocessing scripts and Doc2Vec scripts
    * `scrapers` - Contains web scrapers for notes retieval
    * `visualize` - Contains visualization scripts and PCA
    * `utils.py` - Contains utility methods that can be reused across all modules
* `sql` - SQL scripts for common database maintainance tasks
* `tests` - Contains tests
* `root directory` - Contains runner script for various tasks

## Running
This project is built using Python 3.5

Before running, make sure to install required dependencies by running:
```
pip install -r requirements.txt
```

### Notes import
To import notes into Database:
```
python run_import_notes.py -d <DATA_DIRECTORY_ROOT>
```
This will create a necessary table and import all notes from a given directory (recursively).

To drop an existing Notes table one can run the SQL script located in `sql/clean_notes_table.sql`

### Currencies import
To import currencies into Database:
```
python run_import_currencies.py -b <BASE_CURRENCY> -c <TARGET_CURRENCY> <ARCHIVE_CSV_FILE_PATH>
```
This will create a necessary table and import currency archive from CSV into database.

The CSV is assumed to be formatted as described in <http://www.histdata.com/f-a-q/data-files-detailed-specification/> in `Generic ASCII in M1 Bars`.

For example: If the file contains EUR->PLN currencies archive then base currency is `EUR` and target currency is `PLN`.

To drop an existing Notes table one can run the SQL script located in `sql/clean_currencies_table.sql`

### Scrapers
To run scrapers and fetch articles from the Web:
```
scrapy runspider fxa/scrapers/<SCRAPER_NAME> -o <OUTPUT_FILE>.json
```

Currently the following services are supported:
* Onet Biznes (http://biznes.onet.pl/waluty) - `onet_scraper.py`
* Bankier Waluty (http://www.bankier.pl/waluty/wiadomosci) - `bankier_scraper.py`
* Waluty.com (http://waluty.com.pl/s30-wiadomosci_forex.html) - `waluty_scraper.py`

### Doc2Vec models
In order to create Doc2Vec models make sure all notes are imported in the Database first.
To create a language specific model run:
```
python run_make_doc2vec.py -l <LANG> -o <OUTPUT_FILE>
```
where `LANG` can be either: "en", "es" or "fr".

WARNING: This process is time-consuming! It can take up to few hours to create models for all languages.
The models are also very large. Make sure to have at least 1GB of free disk space for all the models.

### Notes tagging
To tag notes in the DB with currencies and growth information run:
```
python run_notes_tagging.py
```

### ML models
To run ML models:
```
python run_ml_models.py
```

This will run ML algorithms tests and print out results.
Note: This may take a significant amount of time when run on the full notes database.

### Statistics
To run statistical tests:
```
python run_stats.py
```

### Visualizations
To run PCA visualization:
```
python visualize_pca.py
```


### Test
To run tests:
```
pytest
```


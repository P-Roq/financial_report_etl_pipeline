# Automating Financial Reporting Via An ETL Pipeline 

## Introduction

The goal of this pipeline is automate the collection, treatment and storage of financial data on any company registered in the NASDAQ stock market to automatically generate a financial report in PDF format. The original data is sourced via API from the platform [Alpha Vantage](https://www.alphavantage.co/). As an intermediate step, the treated data is stored into a NoSQL database, allowing the access to the data at any time, avoiding the request limitations imposed by the API provider. The financial report 'crunches' the original data which comprises income statements, balance sheets, cash flow and earnings recordings of previous years, into ratios, visual representations and tables that help the user to assess the company's financial health. This pipeline has a two log implementation allowing to trace whether each stage of the pipeline is successfully executed; the stream/standard out only displays basic information while the filed version (activated with a flag) displays full error messages and traceback. 

#### Pipeline stages:

When the data is collected from source via API:
1. Request the data.
2. Clean, trim and tranform data.
3. Push the organized data into a NoSQL remote database.
4. Generate the financial report.

When the data is pulled from remote database:
1. Pull the data.
2. Generate the financial report.


#### Database structure:

A database for this specific pipeline lives in a remote cluster (MongoDB); each collection corresponds to data concerning a single company; documents within the collection store different financial elements: :   
- Company general information (full name, address, industry, sector, etc)
- Latest common indicators (financial metrics and indicators already provided by the original data provider for the latest year, e.g.: market capitalization, price-earning ratio, beta, etc)
- Income statement
- Balance sheet
- Cash Flow
- Earnings 

The financial statements records usually span over a period of 10+ years unless the company's stocks are traded for a shorter duration, in which case the records extend only as far back as the number of years the company's stocks have been traded.




## Generated Report - Example

![page_1](/img/report_example_page_1.jpg)

![page_2](/img/report_example_page_2.jpg)

![page_3](/img/report_example_page_3.jpg)

## Instalation

Python version used: 3.8.19

- Clone the project
- Go to the project's `app` folder directory
- Install a virtual environment for the project with pipenv 
- Create the first project's `.env` file in order to set the root's working path environment variable: 

        $ echo "PYTHONPATH=$/path/to/project/root/" > .env

- Establish the connection with the second `.env` file, stored outside the project's directory, that contains the API key and remote database credentials:

        # Finance API Key
        API_KEY=

        # Mongo DB 
        HOST_DB=
        USER_DB=
        PW_DB=
        CLUSTER=
        DB_NAME=

The path to this `.env` file must be configured in the `src/env_validation.py` module; it is set by default as `f'{config_path}/financial_report_etl_project_config/.env'` where `config_path` refers to a path environment variable. 

## Usage

        usage: main.py [-h] [-cc | -d | -u] [-nr] [-l] [-fl] company

        Multiple options to handle data collection, database management, logging, and report generation.

        positional arguments:
            company               
                The company's symbol iniates the ETL (case-insensitive). It can be used to perform database 
                operations (check/delete collection).

        optional arguments:
            -h, --help            show this help message and exit
            -cc, --check-collection
                Checks if a collection exists in the remote database for the given company.
            -d, --delete          Deletes a collection regarding the specified company from the remote database.
            -u, --update          Flag to indicate whether to update data for the specified collection/company.
            -nr, --no-report      Indicates whether to supress the generation of the report.
            -l, --log             Creates a log file and/or appends log entries to it.
            -fl, --flush-log      
                Flushs the log file before a new ETL run or remote database operation (check/delete collection).

## Other Features

- Reports can be stored at a specific location by filling out the variable `report_directory` in `/app/parameters.yml`; if no path is specified the reports are stored in the `reports` folder by default.
- Similarly, the log file is stored by default in the `app` folder but can be stored else where filling out `log_directory` in `/app/parameters.yml`. 
- The log file is automatically flushed by deafult when it registers 10 runs; the number of runs before flushing can be specified by filling out the `runs_before_flush_log` parameter, alos in `/app/parameters.yml`. 
- A feature allows to identify whether one of the requested JSON files - income statement, balance sheet, etc., is unable to be collected from the source (shuts down the ETL).

### Examples - command and standard output.

#### Successful report generation - source data via API.

    $ python3 app/main.py meta

    $ 2024-04-15 12:29:34,169 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 12:29:36,049 - INFO - No data found in the database for the 
    collection/company: META.
    $ 2024-04-15 12:29:39,820 - INFO - Data successfully collected from source via API.
    $ 2024-04-15 12:29:39,901 - INFO - Data successfully cleaned and transformed.
    $ 2024-04-15 12:29:43,278 - INFO - Data regarding the company META successfully 
    pushed to the remote database.
    $ 2024-04-15 12:29:48,054 - INFO - A report has been generated and stored at 
    /project_root/path/to/reports/financial_report_meta.pdf.


#### Successful report generation - pull from database.

    $ python3 app/main.py -update ibm

    $ 2024-04-25 12:25:39,932 - INFO - Successfull connection to MongoDB.
    $ 2024-04-25 12:25:41,465 - INFO - A collection was found in the database regarding the 
    collection/company: IBM.
    $ 2024-04-25 12:25:44,204 - INFO - Data successfully pulled from the remote database.
    $ 2024-04-25 12:25:49,626 - INFO - A report has been generated and stored at 
    /project_root/path/to/reports/financial_report_ibm.pdf.

#### Unable to connect to remote database.

    $ python3 app/main.py -update ibm

    $ 2024-04-15 13:03:21,730 - ERROR - Unable to connect to MongoDB. 
    Pipeline shuted down.

#### Expired API use.

    $ python3 app/main.py -update ibm

    $ 2024-04-15 13:01:02,623 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 13:01:06,024 - INFO - A collection was found in the database regarding 
    the collection/company: IBM.
    $ 2024-04-15 13:01:06,979 - INFO - Unable to collect data from source via API: rate 
    limit of 25 requests per day exhausted.

#### Unable to collect all the required data elements via API.

    $ python3 app/main.py ibm

    $ 2024-04-15 13:05:15,968 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 13:05:18,857 - INFO - A collection was found in the database regarding 
    the collection/company: IBM.
    $ 2024-04-15 13:05:20,169 - INFO - Data successfully collected from source via API.
    $ 2024-04-15 13:05:25,379 - INFO - Unable to collect data from source via API for the 
    following elements: OVERVIEW, EARNINGS.


#### Successful deletion of a collection.

    $ python3 app/main.py --delete meta

    $ 2024-04-15 07:45:57,369 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 07:45:59,867 - INFO - A collection was found in the database regarding 
    the collection/company: META.
    $ 2024-04-15 07:46:02,084 - INFO - Data regarding the company META successfully deleted
    from the remote database.

#### Unable to delete.

    $ python3 app/main.py --delete nvda

    $ 2024-04-15 07:52:36,511 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 07:52:38,420 - INFO - No data found in the database for the 
    collection/company: NVDA. 


#### Check collection - available.

    $ python3 app/main.py --check-collection tsla

    $ 2024-04-15 09:51:55,922 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 09:51:57,814 - INFO - A collection was found in the database 
    regarding the collection/company: TSLA.


#### Check collection - unavailable.

    $ python3 app/main.py --check-collection amd

    $ 2024-04-15 09:55:44,340 - INFO - Successfull connection to MongoDB.
    $ 2024-04-15 09:55:46,305 - INFO - No data found in the database for 
    the collection/company: AMD.




## License

MIT License
import yaml
import requests
import os
import sys
import re
import pandas as pd
from dotenv import load_dotenv
from arguments import args
from logging_aux import (
    log,
    check_request_all_outputs,
    check_request_limit,
    )

from src.env_validation import settings
from src.utils import convert_camel_to_spaces, check_request_output

load_dotenv()

app_dir = f'{os.getenv("PYTHONPATH")}/app'

src_dir = re.sub(f'{app_dir}/src', '', os.getcwd())

with open(f'{app_dir}/parameters.yml', 'r') as file:
    parameters = yaml.safe_load(file)

company = args.company
url_api = parameters['url']
api_key = settings.api_key

report_name = f'{src_dir}/reports/financial_report_{company.lower()}.pdf'

data_url_parameters = [
    'OVERVIEW',
    'INCOME_STATEMENT',
    'BALANCE_SHEET',
    'CASH_FLOW',
    'EARNINGS'
]

table_names = [
    'overview',
    'income_statement',
    'balance_sheet',
    'cash_flow',
    'earnings',
]

data = {}

data_check = {}

for index, value in enumerate(data_url_parameters):
    full_url = f'{url_api}/query?function={value}&symbol={company}&apikey={api_key}'
    r = requests.get(full_url)
    raw_data = r.json()

    data_check[value] = check_request_output(raw_data)

    if value == 'OVERVIEW':
        check_request_limit(log, raw_data) # we only need to check the request limit once 

        table = pd.DataFrame(raw_data, index=['Overview']).transpose()
        
        table.index = [convert_camel_to_spaces(col) for col in table.index]
        
        table.loc['Data Source', 'Overview'] = url_api
        
        data[table_names[index]] = table
        
    elif value == 'EARNINGS':
        table = pd.concat([pd.DataFrame(raw_data['annualEarnings'][row], index=[row]) for row in range(len(raw_data['annualEarnings']))])
        table = table.set_index(table.columns[0], drop=True)
        table.columns = [convert_camel_to_spaces(col) for col in table.columns]
        
        data[table_names[index]] = table

    elif value not in ['OVERVIEW', 'EARNINGS']:
        table = pd.concat([pd.DataFrame(raw_data['annualReports'][row], index=[row]) for row in range(len(raw_data['annualReports']))])
        table = table.set_index(table.columns[0], drop=True)
        table.columns = [convert_camel_to_spaces(col) for col in table.columns]
        
        data[table_names[index]] = table
        
check_request_all_outputs(log, data_check)
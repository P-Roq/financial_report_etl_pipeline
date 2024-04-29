import math
from typing import Any
from src.data_loader_api import data
from src.utils import insert_new_line


last_year_indicators = [
    'Latest Quarter',
    'Market Capitalization',
    'PERatio',
    'PEGRatio',
    'Book Value',
    'Dividend Per Share',
    'Dividend Yield',
    'Revenue Per Share TTM',
    'Profit Margin',
    'Operating Margin TTM',
    'Diluted EPSTTM',
    'Trailing PE',
    'Forward PE',
    'Price To Sales Ratio TTM',
    'Price To Book Ratio',
    'EVTo Revenue',
    'EVTo EBITDA',
    'Beta',
    'Shares Outstanding',
    'Dividend Date',
    'Ex Dividend Date',
    '52Week High',
    '52Week Low',
    '50Day Moving Average',
    '200Day Moving Average',
]

indicators_map = {
    'Latest Quarter': 'Latest Quarter',
    'Market Capitalization': 'Market Capitalization',
    'Book Value': 'Book Value',
    'Dividend Per Share': 'Dividend Per Share',
    'Dividend Yield': 'Dividend Yield',
    'Revenue Per Share TTM': 'Revenue Per Share TTM',
    'Profit Margin': 'Profit Margin',
    'Operating Margin TTM': 'Operating Margin TTM',
    'Price To Sales Ratio TTM': 'Price To Sales Ratio TTM',
    'Price To Book Ratio': 'Price To Book Ratio',
    'Beta': 'Beta',
    'Shares Outstanding': 'Shares Outstanding',
    'Dividend Date': 'Dividend Date',
    'Diluted EPSTTM': 'Diluted EPS TTM', 
    'PERatio': 'Price-Earnings Ratio',
    'PEGRatio': 'Price/Earnings-To-Growth',
    'Trailing PE': 'Trailing Price-To-Earnings',
    'Forward PE': 'Forward Price-To-Earnings',
    'EVTo Revenue': 'Enterprise-Value To Revenue',
    'EVTo EBITDA': 'Enterprise-Value To EBITDA',
    'Ex Dividend Date': 'Ex-Dividend Date',
    '52Week High': '52 Week High',
    '52Week Low': '52 Week Low',
    '50Day Moving Average': '50 Day Moving Average',
    '200Day Moving Average': '200 Day Moving Average',
}

data['last_year_indicators'] = (
    data['overview']
    .filter(last_year_indicators, axis=0)
    .copy()
    .rename(columns={'Overview': 'Values'})
    )

data['last_year_indicators'].index = data['last_year_indicators']['Values'].index.map(indicators_map,) 

for col in ['Dividend Date', 'Ex-Dividend Date']: 
    if isinstance(data['last_year_indicators'].loc[col, 'Values'], str) is False:
        if math.isnan(data['last_year_indicators'].loc[col, 'Values']):
            data['last_year_indicators'].loc[col, 'Values'] = 'NaN'

#-------------------------------------------------------------------

symbol = data['overview'].loc['Symbol', 'Overview']

elements_overview = [
    'Data Source',
    'Symbol',
    'Asset Type',
    'Name',
    'CIK',
    'Exchange',
    'Currency',
    'Country',
    'Sector',
    'Industry',
    'Address',
    'Fiscal Year End',
    'Latest Quarter',
    ]

data['overview'] = data['overview'].filter(elements_overview, axis=0)

data['overview'].Overview = data['overview'].Overview.map(insert_new_line)

import pandas as pd

def get_left_table(data: pd.DataFrame,) -> pd.DataFrame:

    indicators_table_left = [
        'Market Capitalization',
        'Price-Earnings Ratio',
        'Price/Earnings-To-Growth',
        'Book Value',
        'Dividend Per Share',
        'Dividend Yield',
        'Revenue Per Share TTM',
        'Profit Margin',
        'Operating Margin TTM',
        'Diluted EPS TTM',
    ]

    return data.filter(indicators_table_left, axis=0)


def get_right_table(data: pd.DataFrame,) -> pd.DataFrame:

    indicators_table_right = [
        'Trailing Price-To-Earnings',
        'Forward Price-To-Earnings',
        'Price To Sales Ratio TTM',
        'Price To Book Ratio',
        'Enterprise-Value To Revenue',
        'Enterprise-Value To EBITDA',
        'Beta',
        'Shares Outstanding',
        'Dividend Date',
        'Ex-Dividend Date',
    ]

    return data.filter(indicators_table_right, axis=0)


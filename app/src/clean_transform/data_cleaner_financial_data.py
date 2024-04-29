from src.clean_transform.data_cleaner_overview import data

indicators_income_statement = [
    'Net Income',
    'Total Revenue',
    'Gross Profit',
    'Ebitda',
    'Ebit',
    'Operating Income',
    'Operating Expenses',
    'Interest Expense',
    'Income Before Tax',
    'Research And Development',
    'Comprehensive Income Net Of Tax',
]

indicators_balance = [
    'Total Assets',
    'Total Liabilities',
    'Total Shareholder Equity',
    'Retained Earnings', 
    'Total Current Assets',
    'Total Current Liabilities',
    'Cash And Cash Equivalents At Carrying Value',
    'Inventory',
    'Short Term Debt',
    'Long Term Debt',
]


indicators_cash_flow = [
    'Operating Cashflow',
    'Profit Loss',
    'Change In Receivables',
    'Capital Expenditures',
    'Dividend Payout',
    'Dividend Payout Preferred Stock',
    'Payments For Operating Activities',
    'Proceeds From Operating Activities',
    'Change In Operating Liabilities',
    'Change In Operating Assets',
    'Cashflow From Investment',
    'Cashflow From Financing',
    'Change In Cash And Cash Equivalents',
]

data['income_statement'] = data['income_statement'].filter(indicators_income_statement, axis=1)
data['balance_sheet'] = data['balance_sheet'].filter(indicators_balance, axis=1)
data['cash_flow'] = data['cash_flow'].filter(indicators_cash_flow, axis=1)

for table in data:
    data[table] = data[table].fillna(0)
    data[table] = data[table].replace('None', 0)
    data[table] = data[table].replace('0', 0)
    if table in ['income_statement', 'balance_sheet', 'cash_flow']:
        data[table] = data[table].astype(int)
    
    elif table == 'earnings':
        data['earnings']['Reported EPS'] = data['earnings']['Reported EPS'].astype(float)

#### Income Statement
data['income_statement'] = data['income_statement'].rename(columns={'Research And Development': 'R&D Expenses'},)

#### Balance Sheet
data['balance_sheet']['Total Debt'] = data['balance_sheet']['Short Term Debt'] + data['balance_sheet']['Long Term Debt']

#### Cash Flow
data['cash_flow'] = data['cash_flow'].rename(columns={'Operating Cashflow': 'Operating Cash Flow'})
data['cash_flow'] = data['cash_flow'].rename(columns={'Cashflow From Financing': 'Cash Flow From Financing'})
data['cash_flow'] = data['cash_flow'].rename(columns={'Cashflow From Investment': 'Cash Flow From Investment'})

data['cash_flow']['Net Operating Cash Flow'] = data['cash_flow']['Proceeds From Operating Activities'] - data['cash_flow']['Payments For Operating Activities']

data['cash_flow']['Free Cash Flow'] = data['cash_flow']['Operating Cash Flow'] - data['cash_flow']['Capital Expenditures'] 

#### Earnings
data['earnings']['Reported EPS'] = data['earnings']['Reported EPS'].round(2)


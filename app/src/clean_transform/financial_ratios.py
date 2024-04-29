import pandas as pd

from src.clean_transform.data_cleaner_financial_data import data

ratios = pd.DataFrame(index=data['income_statement'].index)

ratios['Net Profit Margin'] = data['income_statement'].loc[:, 'Net Income'] / data['income_statement'].loc[:, 'Total Revenue']

ratios['Return On Assets (ROA)'] = data['income_statement'].loc[:, 'Net Income'] / data['balance_sheet'].loc[:, 'Total Assets']

ratios['Return On Equity (ROE)'] = data['income_statement'].loc[:, 'Net Income'] / data['balance_sheet'].loc[:, 'Total Shareholder Equity']

ratios['Interest Coverage'] = data['income_statement'].loc[:, 'Ebit'] / data['income_statement'].loc[:, 'Interest Expense']

ratios['Current Ratio'] = data['balance_sheet'].loc[:, 'Total Current Assets'] / data['balance_sheet'].loc[:, 'Total Current Liabilities']

ratios['Quick/Acid-test'] = (data['balance_sheet'].loc[:, 'Total Current Assets'] - data['balance_sheet'].loc[:, 'Inventory']) / data['balance_sheet'].loc[:, 'Total Current Liabilities']

ratios['Earnings Per Share'] = data['earnings']['Reported EPS'][:ratios.shape[0]]

ratios['Debt-To-Equity'] = data['balance_sheet'].loc[:, 'Total Liabilities'] / data['balance_sheet'].loc[:, 'Total Shareholder Equity']
ratios['Debt-To-Equity'] = ratios['Debt-To-Equity'].round(2)

ratios['Cash Flow Coverage'] = data['cash_flow'].loc[:, 'Operating Cash Flow'] / data['income_statement'].loc[:, 'Interest Expense']
ratios['Cash Flow Coverage'] = ratios['Cash Flow Coverage'].round(2)

ratios['Free Cash Flow-To-Equity'] = data['cash_flow'].loc[:, 'Free Cash Flow'] / data['balance_sheet'].loc[:, 'Total Shareholder Equity']

ratios['Dividend Payout Ratio'] = (data['cash_flow']['Dividend Payout'] / data['income_statement']['Net Income']*100)
ratios['Dividend Payout Ratio'] = ratios['Dividend Payout Ratio'].round(2)


ratios = ratios.iloc[:5, :]

data['ratios'] = ratios.copy()
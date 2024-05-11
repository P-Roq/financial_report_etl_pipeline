import os
import yaml
from dotenv import load_dotenv

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.report_build.page_1 import (
    generate_header,
    generate_overview_section,
    generate_ratios_section,
) 
from src.report_build.page_2 import (
    generate_stock_prices_dividends_section,
    generate_last_year_section,
    generate_cash_flow_section,
)
from src.report_build.page_3 import (
    generate_income_statement_section,
    generate_research_development_sheet_section,
    generate_balance_sheet_section,
)

load_dotenv()

root_dir = os.getenv("PYTHONPATH")

reports_dir = root_dir + '/reports'
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir)

with open(f'{root_dir}/app/parameters.yml', 'r') as file:
    parameters = yaml.safe_load(file)


def generate_page_number(c, number: str):
    # Letter coords: (612.0, 792.0).
    c.setFont("Helvetica", 10)
    c.drawString(letter[0]-50, letter[1]-760, number)

def generate_canvas(data_) -> str:
    # Page 1.
    company_name = data_['overview'].Overview['Name']
    symbol = data_['overview'].Overview['Symbol']
    overview_index = [row for row in data_['overview'].index if row not in ['Name', 'Symbol', 'Data Source']]

    if parameters['report_directory']:
        report_directory = f'{parameters["report_directory"]}/financial_report_{symbol.lower()}.pdf'
    else:
        report_directory = f'{root_dir}/reports/financial_report_{symbol.lower()}.pdf'
    
    try:
        c = canvas.Canvas(report_directory)
    except:
        report_directory = f'{root_dir}/reports/financial_report_{symbol.lower()}.pdf'
        c = canvas.Canvas(report_directory)

    generate_page_number(c, '1')
    
    generate_header(c, company_name, data_['overview'].loc['Data Source', 'Overview'],)
    generate_overview_section(c, data_['overview'].filter(overview_index, axis=0))
    generate_ratios_section(c, data_['ratios'])
    c.showPage()
    # Page 2.
    generate_page_number(c, '2')
    generate_last_year_section(c, data_['last_year_indicators']),
    generate_stock_prices_dividends_section(
        c,
        data_['last_year_indicators'],
        data_['ratios']['Dividend Payout Ratio'],
        )
    generate_cash_flow_section(c, data_['cash_flow'])
    c.showPage()
    # Page 3.    
    generate_page_number(c, '3')
    generate_income_statement_section(c, data_['income_statement'])
    generate_research_development_sheet_section(c, data_['income_statement'])
    generate_balance_sheet_section(c, data_['balance_sheet'])
    c.save()

    return report_directory
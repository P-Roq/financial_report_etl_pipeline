import pandas as pd

from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm

from src.utils import insert_new_line
from src.section_auxiliary.balance_sheet_section_aux import (
    get_assets_liabilities_graph,
    get_balance_table,
)
from src.section_auxiliary.income_statement_section_aux import (
    get_income_statement_graph,
    get_income_table,
)
from src.section_auxiliary.research_development_section_aux import (
    get_research_development_graph,
    get_rd_table
)


def generate_income_statement_section(c, income: pd.DataFrame) -> None:
    
    title_coords = (50, 800)

    # Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(
        title_coords[0],
        title_coords[1],
        f'Income Statement'
        )

    #### Graph on the left.
    img = ImageReader(
        get_income_statement_graph(
            income,
            legend_coords=(0.4, -0.1),
            )
        )
    c.drawImage(
        img,
        title_coords[0]-25,
        title_coords[1]-235,
        width=8*cm,
        height=8*cm
        )
    
    #### Table on the right.
    income = get_income_table(income)
    income.index = [insert_new_line(value, 10) for value in income.index]
    columns = list(income.columns)
    columns = [str(col) for col in columns]
    income = [[''] + columns] \
        + list(income.itertuples(index=True, name=None)) \
        + [['M - Millions; K - Thousands; OS - Original Scale.', '', '', '']]

   
    table = Table(
        income,
        colWidths=[4*cm, 2.5*cm, 2.5*cm, 2.5*cm],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (-1, -2), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('ALIGN', (0, -1), (0, -1), 'CENTER'),            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica-Bold'),
            ('SPAN',(0, -1), (-1, -1)),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
        ]
    )

    table.setStyle(style)

    table.wrapOn(c, 2, 2) 
    table.drawOn(
        c,
        title_coords[0]+200,
        title_coords[1]- 215
        )


def generate_research_development_sheet_section(c, income: pd.DataFrame) -> None:
    
    title_coords = (50, 535)

    #### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(
        title_coords[0],
        title_coords[1],
        f'Research And Development'
        )

    #### Graph on the left.
    img = ImageReader(
        get_research_development_graph(
            income,
            legend_coords=(0.415, -0.1),
            )
        )
    c.drawImage(
        img,
        title_coords[0]-25,
        title_coords[1]-235,
        width=8*cm,
        height=8*cm
        )
    
    #### Table on the right.
    rd = get_rd_table(income)
    
    rd.columns = [insert_new_line(value, 5) for value in rd.columns]
    columns = list(rd.columns)
    columns = [str(col) for col in columns]
    rd = [[''] + columns] \
        + list(rd.itertuples(index=True, name=None)) \
        + [['M - Millions; K - Thousands; OS - Original Scale.', '', '', '']]

   
    table = Table(
        rd,
        colWidths=[2*cm, 3*cm, 3*cm,],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (-1, -2), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (0, -1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica-Bold'),
            ('SPAN',(0, -1), (-1, -1)),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
        ]
    )

    table.setStyle(style)

    table.wrapOn(c, 2, 2) 
    table.drawOn(
        c,
        title_coords[0]+260,
        title_coords[1]-225
        )


def generate_balance_sheet_section(c, balance: pd.DataFrame) -> None:
    
    title_coords = (50, 265)

    #### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(
        title_coords[0],
        title_coords[1],
        f'Balance Sheet'
        )

    #### Graph on the left.
    img = ImageReader(
        get_assets_liabilities_graph(
            balance,
            legend_coords=(0.525, -0.1),
            )
        )
    c.drawImage(
        img,
        title_coords[0]-25,
        title_coords[1]-235,
        width=8*cm,
        height=8*cm
        )

    #### Table on the right.
    balance = get_balance_table(balance)
    balance.index = [insert_new_line(value, 10) for value in balance.index]
    columns = list(balance.columns)
    columns = [str(col) for col in columns]
    balance = [[''] + columns] \
        + list(balance.itertuples(index=True, name=None)) \
        + [['M - Millions; K - Thousands; OS - Original Scale.', '', '', '']]
   
    table = Table(
        balance,
        colWidths=[4*cm, 2.5*cm, 2.5*cm, 2.5*cm],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (-1, -2), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'RIGHT'),
            ('ALIGN', (0, -1), (0, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -2), 'Helvetica-Bold'),
            ('SPAN',(0, -1), (-1, -1)),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
        ]
    )

    table.setStyle(style)

    table.wrapOn(c, 2, 2) 
    table.drawOn(
        c,
        title_coords[0]+200,
        title_coords[1]-190
        )
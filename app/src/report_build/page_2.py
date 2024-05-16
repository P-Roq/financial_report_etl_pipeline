import pandas as pd

from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm

from src.utils import insert_new_line
from src.section_auxiliary.cash_flow_section_aux import (
    get_cash_flow_graph,
    indicators_1,
    indicators_2,
    title_1,
    title_2,
    get_cash_flow_table,
)
from src.section_auxiliary.last_year_indicators_section_aux import (
    get_left_table,
    get_right_table,
)
from src.section_auxiliary.stocks_dividends_section_aux import (
    get_stock_prices_graph,
    get_dividend_payout_ratio_graph,
)

def generate_last_year_section(
    c,
    last_year_data: pd.DataFrame,
    ) -> None:
    
    title_coords = (50, 800)

    latest_quarter = last_year_data.loc['Latest Quarter', 'Values']
    
    #### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(
        title_coords[0],
        title_coords[1],
        f'Latest Quarter Indicators: {latest_quarter}',
        )
    
    #### Table on the left.
    data_left = get_left_table(last_year_data)
    data_left.index = [insert_new_line(value, 10) for value in data_left.index]
    data_left = list(data_left.itertuples(index=True, name=None))

   
    table = Table(
        data_left,
        colWidths=[4*cm, 2.5*cm],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]
    )

    table.setStyle(style)

    table.wrapOn(c, 2, 2) 
    table.drawOn(
        c,
        title_coords[0]+25,
        title_coords[1]-260
        )
    
    #### Table on the right.
    data_right = get_right_table(last_year_data)
    data_right.index = [insert_new_line(value, 10) for value in data_right.index]
    data_right = list(data_right.itertuples(index=True, name=None))

    table = Table(
        data_right,
        colWidths=[4*cm, 2.5*cm],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (-1, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]
    )

    table.setStyle(style)

    table.wrapOn(c, 2, 2) 
    table.drawOn(
        c,
        title_coords[0]+280,
        title_coords[1]-271
        )


def generate_stock_prices_dividends_section(
    c,
    last_year_data: pd.DataFrame,
    dividend_data: pd.DataFrame,
    ) -> None:

    section_coords = (50, 585)

    #### Graph on the left.
    graph_width = 8
    graph_height = 5

    img = ImageReader(
        get_stock_prices_graph(
            last_year_data,
            width_=graph_width,
            height_=graph_height,
            ),
        )
    c.drawImage(
        img,
        section_coords[0],
        section_coords[1]-229,
        width=graph_width*cm,
        height=graph_height*cm
        )
    

    #### Graph on the right.
    graph_width = 8
    graph_height = 5

    img = ImageReader(
        get_dividend_payout_ratio_graph(
            dividend_payout_ratio=dividend_data,
            width_=graph_width,
            height_=graph_height,
            )
        )
    c.drawImage(
        img,
        section_coords[0]+250,
        section_coords[1]-225,
        width=graph_width*cm,
        height=graph_height*cm
        )


def generate_cash_flow_section(c, data: pd.DataFrame) -> None:
    
    title_coords = (50, 325)

    ### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(
        title_coords[0],
        title_coords[1],
        f'Cash Flow'
        )
    
    ### Graphs on the left.
    graph_width = 8
    graph_height = 4.5

    img = ImageReader(
        get_cash_flow_graph(
            data,
            indicators_1, 
            title_1,
            line_colors=('red', 'blue'),
            legend_coords=(0.45, -0.1),
            ),
        )
    c.drawImage(
        img,
        title_coords[0]-25,
        title_coords[1]-140,
        width=graph_width*cm,
        height=graph_height*cm
        )
    
    img = ImageReader(
        get_cash_flow_graph(
            data,
            indicators_2,
            title_2,
            line_colors=('green', 'orange'),
            legend_coords=(0.56, -0.1),
        )
    )
    c.drawImage(
        img,
        title_coords[0]-25,
        title_coords[1]-275,
        width=graph_width*cm,
        height=graph_height*cm
        )
    
    #### Table on the right.
    cash_flow = get_cash_flow_table(data)
    cash_flow.index = [insert_new_line(value, 10) for value in cash_flow.index]
    columns = list(cash_flow.columns)
    columns = [str(col) for col in columns]
    cash_flow = [[''] + columns] \
        + list(cash_flow.itertuples(index=True, name=None)) \
        + [['M - Millions; K - Thousands; OS - Original Scale.', '', '', '']]

   
    table = Table(
        cash_flow,
        colWidths=[4*cm, 2.5*cm, 2.5*cm, 2.5*cm],
        rowHeights=None,
        )

    style = TableStyle(
        [
            ('SIZE', (0, 0), (-1, -1), 9),
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
        title_coords[1]-215
        )
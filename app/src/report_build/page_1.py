import pandas as pd
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm

from src.section_auxiliary.finantial_ratios_section_aux import get_heatmap_ratio


def generate_header(c, enterprise_name_: str, source_url: str,) -> None:
    # Title
    title = 'Financial Report'
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(letter[0] / 2, letter[1] - 20, title)

    # Subtitle
    subtitle = f'Enterprise: {enterprise_name_}'
    c.setFont("Helvetica", 15)
    c.drawCentredString(letter[0] / 2, letter[1] - 50, subtitle)

    # Data source
    data_source = f'Data source / API: {source_url}' 
    c.setFont("Helvetica", 10)
    c.drawString(50, letter[1] - 80, data_source)

    # Date
    date = datetime.now().strftime('%Y-%m-%d')
    c.setFont("Helvetica", 10)
    c.drawString(50, letter[1] - 100, f'Date of extraction: {date}')

def generate_overview_section(c, overview: pd.DataFrame) -> None:
    first_row_coords = (120, 220)

    #### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, first_row_coords[1]+440, f'Overview')
        
    #### Table.
    overview = overview.loc[:, [col for col in overview.columns if col != 'Data Source']]    
    overview = list(overview.itertuples(index=True, name=None))
    table = Table(overview, colWidths=[100, 250], rowHeights=None,)

    style = TableStyle(
        [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]
    )

    table.setStyle(style)

    # Each additional line in table adds 12 points in height to the table, ceteris paribus.
    # The smallest table possible has 162 points of height. 
    width, height = table.wrap(0, 0)

    discount_height = 0
    for i in range(0, 6+1):
        extra_height = i*12
        if height == 162 + extra_height: 
            discount_height += extra_height
            break 

    table.wrapOn(c, 2, 2)
    table.drawOn(c, 50, 490 - extra_height)


def generate_ratios_section(c, ratios: pd.DataFrame) -> None:
    ratios = ratios.drop(columns='Dividend Payout Ratio')
    
    first_row_coords = (120, 220)

    #### Title.
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, first_row_coords[1]+185, f'Financial Ratios')
    
    #### Heatmaps.
    i = 0
    j = 0
    for idx, col in enumerate(ratios.columns):
        if idx >= 5:
            j = 180
            if idx == 5:
                i = 0

        if (idx == 0) or (idx == 5):
            ylabels_ = True
            width_ = 2.5 
        else:
            ylabels_ = False 
            width_ = 2

        img = ImageReader(get_heatmap_ratio(ratios, col, ylabels_))
        c.drawImage(
            img,
            first_row_coords[0]+i,
            first_row_coords[1]-j,
            width=width_*cm,
            height=6*cm
            )
        
        if (idx == 0) or (idx == 5):
            i += 80
        else:
            i += 70
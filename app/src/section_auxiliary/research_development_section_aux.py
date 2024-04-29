import tempfile
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Iterable
from src.utils import scale_values

def get_research_development_graph(data: pd.DataFrame, legend_coords: Iterable) -> None:
    
    data = data.fillna(0)

    indicators = [
        'Total Revenue',
        'Operating Income',
        'R&D Expenses',
    ]

    rd = pd.DataFrame(index=data.index)

    rd['R&D Intensity Ratio'] = data['R&D Expenses'] / data['Total Revenue']
    rd['R&D Operating\nIncome Ratio'] = data['R&D Expenses'] / data['Operating Income']

    fig, ax_ = plt.subplots(figsize=(6, 6)) 

    ax_.set_title('R&D Ratios (Last 10 Years)')

    rd.index = pd.Categorical([int(i[:4]) for i in list(rd.index)])

    rd = rd.sort_index(ascending=False).iloc[:10, :]

    columns = rd.columns

    sns.axes_style("darkgrid")
    colors = ['purple', 'red',]

    for idx, col in enumerate(columns):
        try:
            sns.lineplot(
                rd[columns[idx]],
                ax=ax_,
                color=colors[idx],
                label=columns[idx]
                )
        except:
            pass

    ax_.grid()
    ax_.set_ylabel('')
    ax_.legend(bbox_to_anchor=(legend_coords[0], legend_coords[1]))

    try:
        ax_.set_xticks(rd.index[np.arange(0, 10, 2)])
    except:
        ax_.set_xticks(rd.index)

    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name


def get_rd_table(data: pd.DataFrame, keep_na=True) -> pd.DataFrame:
    
    rd_table = data.filter(['R&D Expenses'], axis=1).copy().iloc[:10, :]
    
    rd_table = scale_values(rd_table, keep_na=True)

    rd_table.index = [int(i[:4]) for i in rd_table.index]

    rd_table = rd_table.sort_index(ascending=True)

    rd_table['YoY % Change'] = rd_table.pct_change(fill_method=None, axis=0).round(2)

    rd_table = rd_table.sort_index(ascending=False)
    
    def fill_rows(table: pd.DataFrame) -> pd.DataFrame:
        """Fill rows with NaN if the original does not have a registry
        for all the past 10 years. The goal is to have alawys a table
        for 10 rows, so that when building the report, it stays in the
        same coordinates, instead of adjusting the coordinates if the 
        number of rows/years vary from company to company.
        """
        latest_year = table.index[0]
        year_range = [i for i in range(latest_year-9, latest_year)]
        for idx, year in enumerate(year_range):
            if year not in table.index:
                table.loc[year, :] = (None, None,)
        
        return table.sort_index(ascending=False) 

    return fill_rows(rd_table)
from typing import Iterable
import tempfile
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from src.utils import scale_values, remove_columns_excessive_na

indicators_1 = (
    'Cash Flow From Investment',
    'Cash Flow From Financing',
)   

indicators_2 = (
    'Change In Cash And Cash Equivalents',
    'Change In Receivables',
)

title_1 = 'Cash Flow By Category'
title_2 = 'Cash Flow Changes'

def get_cash_flow_graph(
    cashflow: pd.DataFrame,
    indicators_: Iterable,
    title_: str,
    line_colors: Iterable[str],
    legend_coords: Iterable[int],
    ) -> None:
    
    cashflow_1 = cashflow.copy()

    fig, ax_ = plt.subplots(figsize=(8, 4)) 

    ax_.set_title(title_)

    cashflow_1 = cashflow_1.filter(indicators_, axis=1).iloc[:10, :]
    
    cashflow_1 = remove_columns_excessive_na(cashflow_1)

    cashflow_1.index = [int(i[:4]) for i in list(cashflow_1.index)]

    cashflow_1 = cashflow_1.sort_index(ascending=False)

    cashflow_1 = scale_values(cashflow_1, keep_na=False)

    columns = cashflow_1.columns

    sns.axes_style("darkgrid")
    line_styles = ['-', '-',]

    for idx, col in enumerate(columns):
        try:
            sns.lineplot(
                cashflow_1[columns[idx]],
                ax=ax_,
                linestyle=line_styles[idx],
                color=line_colors[idx],
                label=columns[idx],
                )
        except:
            pass

    ax_.grid()
    ax_.set_ylabel('USD')
    ax_.legend(bbox_to_anchor=(legend_coords[0], legend_coords[1]))
    
    try:
        ax_.set_xticks(cashflow_1.index[np.arange(0, 10, 2)])
    except:
        ax_.set_xticks(cashflow_1.index)
                       
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name


def get_cash_flow_table(data: pd.DataFrame, keep_na=True) -> pd.DataFrame:
    data_1 = data.copy()
    
    indicators = [
        'Operating Cash Flow',
        'Change In Receivables',
        'Capital Expenditures',
        'Dividend Payout',
        'Profit Loss',
        ]
     
    data_table = data_1[indicators].iloc[:1+1, :]
    
    data_table = scale_values(data_table, keep_na=True)

    data_table.index = [int(i[:4]) for i in data_table.index]

    data_table = data_table.sort_index().transpose()

    pct_change = data_table.pct_change(fill_method=None, axis=1).round(2)

    data_table['% Change'] = pct_change.iloc[:, -1]

    return data_table
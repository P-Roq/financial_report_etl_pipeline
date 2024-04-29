import tempfile
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Iterable
from src.utils import scale_values, remove_columns_excessive_na


def get_assets_liabilities_graph(balance: pd.DataFrame, legend_coords: Iterable) -> None:
    balance_1 = balance.copy()
    
    indicators = [
            'Total Assets',
            'Total Liabilities', 
            'Total Current Assets',
            'Total Current Liabilities',
        ]

    fig, ax_ = plt.subplots(figsize=(6, 6)) 

    ax_.set_title('Assets and Liabilities (Last 10 Years)')

    balance_1 = balance_1.filter(indicators, axis=1).iloc[:10, :]

    balance_1 = remove_columns_excessive_na(balance_1)

    balance_1.index = [int(i[:4]) for i in list(balance_1.index)]

    balance_1 = balance_1.sort_index(ascending=False)

    balance_1 = scale_values(balance_1, keep_na=False)

    columns = balance_1.columns

    sns.axes_style("darkgrid")
    line_styles = ['-', '-', '--', '--',]
    colors = ['darkblue', 'darkred', 'skyblue', 'red']

    for idx, col in enumerate(columns):
        try:
            sns.lineplot(
                balance_1[columns[idx]],
                ax=ax_,
                linestyle=line_styles[idx],
                color=colors[idx],
                label=columns[idx],
                )
        except:
            pass

    ax_.grid()
    ax_.set_ylabel('USD')
    ax_.legend(bbox_to_anchor=(legend_coords[0], legend_coords[1]))

    try:
        ax_.set_xticks(balance_1.index[np.arange(0, 10, 2)])
    except:
        ax_.set_xticks(balance_1.index)

    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name



def get_balance_table(balance: pd.DataFrame, keep_na=True) -> pd.DataFrame:
    balance_1 = balance.copy()
    
    indicators = [
        'Total Shareholder Equity',
        'Retained Earnings',
        'Cash And Cash Equivalents At Carrying Value',
        'Inventory'
        ]
     
    balance_table = balance_1[indicators].iloc[:1+1, :]
    
    balance_table = scale_values(balance_table, keep_na=True)

    balance_table.index = [int(i[:4]) for i in balance_table.index]

    balance_table = balance_table.sort_index().transpose()

    pct_change = balance_table.pct_change(fill_method=None, axis=1).round(2)

    balance_table['% Change'] = pct_change.iloc[:, -1]

    return balance_table
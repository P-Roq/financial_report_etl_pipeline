import tempfile
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Iterable
from src.utils import scale_values,remove_columns_excessive_na

def get_income_statement_graph(income: pd.DataFrame, legend_coords: Iterable) -> None:
    income_1 = income.copy()
    
    indicators = [
            'Net Income',
            'Total Revenue',
            'Gross Profit',
            'Ebitda',
        ]

    fig, ax_ = plt.subplots(figsize=(6, 6)) 

    ax_.set_title('Performance Indicators (Last 10 Years)')

    income_1 = income_1[indicators].filter(indicators, axis=1).iloc[:10, :]

    income_1 = remove_columns_excessive_na(income_1)

    income_1.index = [int(i[:4]) for i in list(income_1.index)]

    income_1 = income_1.sort_index(ascending=False)

    income_1 = scale_values(income_1, keep_na=False)

    columns = income_1.columns

    sns.axes_style("darkgrid")
    colors = ['blue', 'red', 'green', 'orange']

    for idx, col in enumerate(columns):
        try:
            sns.lineplot(
                income_1[columns[idx]],
                ax=ax_,
                color=colors[idx],
                label=columns[idx]
                )
        except:
            pass

    ax_.grid()
    ax_.set_ylabel('USD')
    ax_.legend(bbox_to_anchor=(legend_coords[0], legend_coords[1]))
    
    try:
        ax_.set_xticks(income_1.index[np.arange(0, 10, 2)])
    except:
        ax_.set_xticks(income_1.index)
        
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name


def get_income_table(income: pd.DataFrame, keep_na=True) -> pd.DataFrame:
    income_1 = income.copy()
    
    indicators = [
        'Operating Income',
        'Operating Expenses',
        'Interest Expense',
        'Income Before Tax',
        'Comprehensive Income Net Of Tax'
        ]
     
    income_table = income_1[indicators].iloc[:1+1, :]
    
    income_table = scale_values(income_table, keep_na=True)

    income_table.index = [int(i[:4]) for i in income_table.index]

    income_table = income_table.sort_index().transpose()

    pct_change = income_table.pct_change(fill_method=None, axis=1).round(2)

    income_table['% Change'] = pct_change.iloc[:, -1]


    return income_table
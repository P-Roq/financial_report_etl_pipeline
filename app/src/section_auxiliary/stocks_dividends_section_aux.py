import tempfile
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Union

from src.utils import insert_new_line


def get_stock_prices_graph(
    data: pd.DataFrame,
    width_: Union[int, float],
    height_: Union[int, float],
    ) -> pd.DataFrame:

    year = data.loc['Latest Quarter', 'Values'][:4]

    stock_prices = [
        '52 Week High',
        '52 Week Low',
        '50 Day Moving Average',
        '200 Day Moving Average',
    ]

    data = data.filter(stock_prices, axis=0).astype(float)

    data.index = [insert_new_line(i, 10) for i in data.index]

    fig, ax_ = plt.subplots(figsize=(width_, height_))

    ax_.set_title(f'Stock Prices ({year})', size=15, y=1.25)

    colors = ['blue', 'lightblue', 'green', 'lightgreen']

    ax_ = sns.barplot(
        x=pd.Categorical(data.index),
        y=data.Values,
        hue=data.index,
        palette=colors,
        )

    ax_.set_ylabel('USD')
    ax_.set_xlabel('')

    for container, label in zip(ax_.containers, data.Values):
        ax_.bar_label(
            container,
            labels=[label],
            fontsize=10,
            padding=2,
            )

    ax_.spines['top'].set_visible(False)
    ax_.spines['right'].set_visible(False)
    ax_.spines['left'].set_visible(False)

    ax_.yaxis.set_ticks([0])

    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name


def get_dividend_payout_ratio_graph(
    dividend_payout_ratio: pd.Series,
    width_: Union[int, float],
    height_: Union[int, float],
    ) -> pd.DataFrame:

    fig, ax_ = plt.subplots(figsize=(width_, height_))

    ax_.set_title('Dividend Price Ratio', size=15, y=1.25)
    
    ax_ = sns.barplot(
        x=pd.to_datetime(dividend_payout_ratio.index),
        y=dividend_payout_ratio,
        hue=pd.to_datetime(dividend_payout_ratio.index),
        )
    
    ax_.yaxis.set_ticks([0])

    ax_.set_ylabel('')
    ax_.set_xlabel('')

    bar_labels = [f'{i}%' for i in dividend_payout_ratio.tolist()]

    for idx, container, label in zip(range(0, len(bar_labels)), ax_.containers, bar_labels):
        if dividend_payout_ratio.tolist()[idx] >= 0:
            padding_=2
        else:
            padding_=-15
        
        ax_.bar_label(
            container,
            labels=[label],
            fontsize=10,
            padding=padding_,
            )

    one_zero = [True for i in dividend_payout_ratio.tolist() if i == 0]
    one_negative = [True for i in dividend_payout_ratio.tolist() if i < 0]
    one_positive = [True for i in dividend_payout_ratio.tolist() if i > 0]

    if (any(one_zero) and any(one_negative)) or (any(one_positive) and any(one_negative)):
        ax_.axhline(y=0, color='black', linestyle='-')
        ax_.spines['top'].set_visible(False)
        ax_.spines['right'].set_visible(False)
        ax_.spines['left'].set_visible(False)
        ax_.spines['bottom'].set_visible(False)
    
    else:
        ax_.spines['top'].set_visible(False)
        ax_.spines['right'].set_visible(False)
        ax_.spines['left'].set_visible(False)
    

    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name
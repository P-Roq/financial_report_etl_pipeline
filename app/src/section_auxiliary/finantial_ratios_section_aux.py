import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile

def get_heatmap_ratio(
    data: pd.DataFrame,
    ratio: str,
    ylabels: bool,
    ):

    fig, ax_ = plt.subplots(figsize=(3, 6))

    ax_.set_title(ratio, size=15)
    ax_.set_ylabel('')

    data[ratio].index = pd.to_datetime(data[ratio].index, format='%Y-%m-%d').strftime('%Y')

    data = pd.DataFrame({ratio: data[ratio].values}, index=list(data[ratio].index))

    data = data.fillna(0)
    
    if ratio == 'Interest Coverage':
        fontsize_ = 18
    else:
        fontsize_ = 20

    if ratio == 'Debt-To-Equity':    
        colormap_ = 'rocket_r'
    else:
        colormap_ = 'rocket'

    sns.heatmap(
        data,
        annot=data,
        cmap=colormap_,
        annot_kws={"fontsize": fontsize_},
        fmt='.2f',
        cbar=False,
        linewidths=2,
        yticklabels=ylabels,
        xticklabels='',
        ax=ax_,
        )

    ax_.set_yticklabels(ax_.get_yticklabels(), rotation=0, fontsize=15)
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    
    plt.savefig(temp_file.name, bbox_inches="tight")
    
    temp_file.close()
    
    return temp_file.name

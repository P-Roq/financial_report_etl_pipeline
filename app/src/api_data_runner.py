from logging_aux import (
    log,
    log_exceptions
    )
from src.clean_transform.financial_ratios import data

@log_exceptions(
    log,
    'Data successfully cleaned and transformed.',
    'Unable to clean and/or transform the collected data.',
    exit_app=True
    )
def get_data():
    return data
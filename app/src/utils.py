import pandas as pd
import re
from typing import Any, Union
from dotenv import load_dotenv
import os
import yaml

load_dotenv()

def insert_new_line(value: Any, threshold_: int = 30) -> Any:

    def divide_string(value: str, threshold: int) -> str:    
        left = value[:threshold]
        right = value[threshold:]
        
        try:
            right = re.sub('\s', '\n', right, 1)
        except:
            pass
        return left + right

    if isinstance(value, str):

        multiplier = 1
        length = len(value)

        while (threshold_ < length) and (multiplier < 10):
            value = divide_string(value, threshold_)
            multiplier += 1
            threshold_ = threshold_ * multiplier
        else:
            return value
    
    return value

def convert_camel_to_spaces(string: str) -> str:
    """Convert camel case into spaces between words.
    First letter to uppser case.
    """

    try:
        string = re.sub(r'([a-z])([A-Z])', r'\1 \2', string) 
    except:
        pass

    try:
        first_char = string[0].upper()
        rest = string[1:]
        string = first_char + rest
    except:
        pass

    return string 


def scale_values(data: pd.DataFrame, keep_na: bool) -> pd.DataFrame:
    """To avoid series with large currency numbers by scaling and 'tagging'
    the column's name: from 4 to 6 digits divide by a thousand (K);
    over 6 digits divide by a million (M)."""

    data = data.copy().astype(float)

    if keep_na is False:
        data = data.fillna(0)


    columns = list(data.columns)

    for idx, col in enumerate(columns):
        mean = str(int(data.loc[:, col].mean()))

        if 4 <= len(mean) <= 6:
            columns[idx] = columns[idx] + ' (K)'
            data.loc[:, col] = data.loc[:, col] / 1000

        elif len(mean) >= 7:
            columns[idx] = columns[idx] + ' (M)'
            data.loc[:, col] = data.loc[:, col] / 1000000

        elif len(mean) < 6:
            columns[idx] = columns[idx] + ' (OS)'

    data.columns = columns

    return data


def remove_columns_excessive_na(data: pd.DataFrame) -> pd.DataFrame:

    length = data.shape[0]
    half = length / 2

    to_remove = []

    for col in data.columns:
        count_na = data[col].isna().sum()
        if count_na > half:
            to_remove.append(col)

    return data[[col for col in data.columns if col not in to_remove]]



def center_image(image_width, letter_):
    
    page_width, _ = letter_

    x = (page_width - image_width) / 2

    return x

def check_request_output(output,):

    failed_request_output = {
        'Information': 'Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits.'
        }

    condition_1 = output == {}
    condition_2 = output == failed_request_output 

    if condition_1 or condition_2 is True:
        return False
    else:
        return True
    

def flush_log(log_runs_threshold: Union[int, None], flush_log: bool):

    if log_runs_threshold is None:
        log_runs_threshold = 10

    app_dir = f'{os.getenv("PYTHONPATH")}/app'

    with open(f'{app_dir}/parameters.yml', 'r') as file:
        parameters = yaml.safe_load(file)

    log_dir = parameters['log_directory']

    if log_dir is None:
        log_dir = app_dir

    path_to_log = log_dir + '/app.log'

    check_log_condition = os.path.exists(path_to_log) and os.path.isdir(log_dir)

    if flush_log:
        with open(path_to_log, "w") as f:
            f.truncate(0)

    elif check_log_condition:
        runs = 0

        with open(path_to_log, 'r') as file:
            log = file.readlines() 
    
        for line in log:
            if re.findall('ETL started', line,) or re.findall('Maintenance', line,):
                runs += 1

        if runs >= log_runs_threshold:
            with open(path_to_log, "w") as f:
                f.truncate(0)

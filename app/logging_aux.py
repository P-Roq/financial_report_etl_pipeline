import yaml
import os
from dotenv import load_dotenv
import sys
import logging
from typing import Callable, Dict, Union
from arguments import args
from src.utils import flush_log


load_dotenv()

app_dir = f'{os.getenv("PYTHONPATH")}/app'

with open(f'{app_dir}/parameters.yml', 'r') as file:
    parameters = yaml.safe_load(file)

log_dir = parameters['log_directory']
runs_threshold = parameters['runs_before_flush_log']

if log_dir is None:
    log_dir = app_dir

class Loggers:
    loggers = {'stream': None, 'file': None} 
    def __init__(
            self,
            log_dir_: str,
            runs_threshold_: Union[int, None],
            flush_log_: bool = False, 
            log_file: bool = False,
            ) -> None:
        
        flush_log(runs_threshold_, flush_log_)

        path_to_log = f'{log_dir_}/app.log'
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # Simpler format for std output

        stream_logger = logging.getLogger('stream_logger')
        stream_logger.setLevel(logging.INFO) 
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_logger.addHandler(stream_handler)
        self.loggers['stream'] = stream_logger  

        matplotlib_logger = logging.getLogger('matplotlib')
        matplotlib_logger.setLevel(logging.ERROR)  
        matplotlib_handler = logging.StreamHandler()
        matplotlib_logger.addHandler(matplotlib_handler)
        
        if log_file:
            file_logger = logging.getLogger('file_logger')
            file_logger.setLevel(logging.INFO) 
            file_handler = logging.FileHandler(path_to_log)
            file_handler.setFormatter(formatter)
            file_logger.addHandler(file_handler)
            self.loggers['file'] = file_logger  


log = Loggers(log_dir, runs_threshold, args.flush_log, args.log) 


def log_exceptions(
    log_: Loggers,
    success_message: str,
    stream_error_message: Union[None, str] = None,
    exit_app: bool = False,
    ):
    """A decorator that logs exceptions raised by the decorated function."""
    

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                output = func(*args, **kwargs)
                
                for logger_type in log_.loggers:
                    if log_.loggers[logger_type]:
                        log_.loggers[logger_type].info(success_message)

                return output
            
            except Exception as e:
                log_.loggers['stream'].error('%s', stream_error_message, exc_info=False)

                if log_.loggers['file']:
                    log_.loggers['file'].error('%s', str(e), exc_info=True)

                if exit_app:
                    sys.exit(1)

        return wrapper
    
    return decorator


def log_check_data_availability(log_: Loggers, check_collection_: bool, update_:bool, company_: str) -> None:
    if check_collection_:
        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].info(
                    f'A collection was found in the database regarding the collection/company: {company_.upper()}.',
                    )
    else:
        if update_:
            for logger_type in log_.loggers:
                if log_.loggers[logger_type]:
                    log_.loggers[logger_type].info(
                        f'No data found in the database for the collection/company: {company_.upper()}. Requesting data from source via API.',
                        )
        else:
            for logger_type in log_.loggers:
                if log_.loggers[logger_type]:
                    log_.loggers[logger_type].info(
                        f'No data found in the database for the collection/company: {company_.upper()}.',
                        )


def log_generate_canvas(log_: Loggers, func: Callable, data_: Dict, no_report_flag: bool) -> None:
    if no_report_flag is False:
        report_directory = func(data_)
        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].info(
                    f'A report has been generated and stored at {report_directory}.',
                    )
    else:
        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].info(
                    'The report generation has been suppressed.',
                    )


def check_request_all_outputs(log_: Loggers, data_check_: Dict[str, bool]):

    if all([data_check_[boolean] for boolean in data_check_]):
        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].info(
                    'Data successfully collected from source via API.'
                    )
    else:
        faulty_data = [boolean for boolean in data_check_ if data_check_[boolean] is False]

        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].error(
                    f'Unable to collect data from source via API for the following elements: {", ".join(faulty_data)}.',
                    )
        sys.exit(1)


def check_request_limit(log_: Loggers, output,):

    failed_request_output = {
        'Information': 'Thank you for using Alpha Vantage! Our standard API rate limit is 25 requests per day. Please subscribe to any of the premium plans at https://www.alphavantage.co/premium/ to instantly remove all daily rate limits.'
        }

    condition = output == failed_request_output 

    if condition:
        for logger_type in log_.loggers:
            if log_.loggers[logger_type]:
                log_.loggers[logger_type].error(
                    'Unable to collect data from API: rate limit of 25 requests per day exhausted.',
                    )
        sys.exit(1)
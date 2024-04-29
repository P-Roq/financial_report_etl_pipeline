from logging_aux import (
    Loggers,
    log,
    log_generate_canvas,
    log_check_data_availability,
)
from arguments import args
from src.env_validation import db_settings
from src.database import (
    uri,
    test_connection,
    check_data_availability,
    insert_data,
    pull_data,
    update_data,
    delete_data,
    )
from src.report_build.report_assembly import generate_canvas


def main(
        log_: Loggers,
        company: str,
        update: bool = False,
        no_report: bool = False,
        check_collection: bool = False,
        drop_collection: bool = False,
        ) -> None:
    
    company = company.upper()
    
    if check_collection:
        if log_.loggers['file']:
            log_.loggers['file'].info('%s', 'Maintenance.', exc_info=False)

        test_connection(uri)
        _check_collection = check_data_availability(uri, db_settings.db_name, company)
        log_check_data_availability(log_, _check_collection, update, company)

    elif drop_collection:
        if log_.loggers['file']:
            log_.loggers['file'].info('%s', 'Maintenance.', exc_info=False)

        test_connection(uri)
        _check_collection = check_data_availability(uri, db_settings.db_name, company)
        log_check_data_availability(log_, _check_collection, update, company)
        if _check_collection:
            delete_data(uri, db_settings.db_name, company)

    else:    
        if log_.loggers['file']:
            log_.loggers['file'].info('%s', 'ETL started.', exc_info=False)

        
        test_connection(uri)

        _check_collection = check_data_availability(uri, db_settings.db_name, company)

        log_check_data_availability(log_, _check_collection, update, company)

        if _check_collection:
            if update:
                from src.api_data_runner import get_data            
                data = get_data()
                update_data(uri, db_settings.db_name, data)
            else:
                data = pull_data(uri, db_settings.db_name, company)
        else:
            from src.api_data_runner import get_data            
            data = get_data()
            insert_data(uri, db_settings.db_name, data)
        
        log_generate_canvas(log_, generate_canvas, data, no_report)

if __name__ == "__main__":
    main(
        log,
        args.company,
        args.update,
        args.no_report,
        args.check_collection,
        args.drop_collection,
        )

import argparse
import sys
 
parser = argparse.ArgumentParser(
    description='Multiple options to handle data collection, database management, logging, and report generation.',
    )

exclusive_group = parser.add_mutually_exclusive_group(required=False)

exclusive_group.add_argument(
    '-cc',
    '--check-collection',
    action='store_true',
    dest='check_collection',
    help='Checks if a collection exists in the remote database for the given company.'
    )

exclusive_group.add_argument(
    '-d',
    '--delete',
    action='store_true',
    dest='drop_collection',
    help='Deletes a collection regarding the specified company from the remote database.',
    )

exclusive_group.add_argument(
    '-u',
    '--update',
    action='store_true',
    help='Flag to indicate whether to update data for the specified collection/company.',
    )

parser.add_argument(
    'company',
    help="The company's symbol iniates the ETL (case-insensitive). It can be used to perform database operations (check/delete collection).",
    )

parser.add_argument(
    '-nr',
    '--no-report',
    action='store_true',
    dest='no_report',
    help='Indicates whether to supress the generation of the report.',
    )

parser.add_argument(
    '-l',
    '--log',
    action='store_true',
    dest='log',
    help='Creates a log file and/or appends log entries to it.',
    )

parser.add_argument(
    '-fl',
    '--flush-log',
    action='store_true',
    dest='flush_log',
    help='Flushs the log file before a new ETL run or remote database operation (check/delete collection).',
    )

def validate_args(args):
    try:
        if (args.drop_collection and args.no_report) or (args.check_collection and args.no_report):
            raise argparse.ArgumentError(None, 'main.py: error: -nr/--no_report cannot be used with arguments -cc/--check-collection, -d/--delete')
    except argparse.ArgumentError as e:
        print(str(e))
        sys.exit(1)

args = parser.parse_args()

parser.set_defaults(validate=validate_args(args))



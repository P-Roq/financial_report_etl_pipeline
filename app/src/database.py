from typing import Dict
import pandas as pd
from logging_aux import log, log_exceptions
from arguments import args
from src.env_validation import db_settings

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


company = args.company.upper()

uri = f'mongodb+srv://{db_settings.user_db}:{db_settings.pw_db}@{db_settings.cluster.lower()}.q5hk3xy.mongodb.net/?retryWrites=true&w=majority&appName={db_settings.cluster}'
 
@log_exceptions(
    log_=log, 
    success_message='Successfull connection to MongoDB.',
    stream_error_message='Unable to connect to MongoDB. Pipeline shuted down.',
    exit_app=True,
    )
def test_connection(uri_: str) -> str:
    client = MongoClient(uri, server_api=ServerApi('1'))
    client.admin.command('ping')
    client.close()


def check_data_availability(uri_: str, db_name: str, collection: str) -> bool:
    client = MongoClient(uri_, server_api=ServerApi('1'))
    db = client[db_name]
    collections = db.list_collection_names()
    client.close()

    return collection in collections


@log_exceptions(
    log,
    f'Data regarding the company {company} successfully pushed to the remote database.',
    f'Unable to insert data into the remote database.',
    exit_app=True,
    )
def insert_data(
    uri_: str,
    db_name: str,
    data: Dict[str, pd.DataFrame],
    ) -> None:
    
    client = MongoClient(uri_, server_api=ServerApi('1'))
    db = client[db_name]
    company = data['overview'].Overview['Symbol'].upper()
    collection = db[company]
    tables = list(data.keys())
    
    for table_name in tables:
        result = collection.insert_one(
            {table_name: data[table_name].to_dict()}
            ) 
    
    client.close()
    

@log_exceptions(
    log,
    f'Data updated successfully for the collection/company: {company}.',
    f'Unable to update the data for the collection/company: {company}.',
    exit_app=False
    )
def update_data(
    uri_: str,
    db_name: str,
    data: Dict[str, pd.DataFrame],
    ) -> None:
    
    client = MongoClient(uri_, server_api=ServerApi('1'))
    db = client[db_name]
    company = data['overview'].Overview['Symbol'].upper()
    collection = db[company]
    cursor = collection.find()
    
    for doc in cursor:
        table_name = [key for key in list(doc.keys()) if key != '_id'][0]
        collection.update_one({"_id": doc['_id']}, {"$set": {table_name: data[table_name].to_dict()}})

    client.close()


@log_exceptions(
    log,
    'Data successfully pulled from the remote database.',
    'Unable to pull data from remote database.',
    exit_app=True,
    )
def pull_data(
    uri_: str,
    db_name: str,
    collection_name: str,        
    ) -> Dict[str, pd.DataFrame]:

    tables = [
        'overview',
        'income_statement',
        'balance_sheet', 
        'cash_flow',
        'earnings',
        'last_year_indicators',
        'ratios',
        ]

    client = MongoClient(uri_, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    data = {}

    for doc in cursor:
        first_order_keys = list(doc.keys())
        for table_name in tables:
            if table_name in first_order_keys:
                data[table_name] = pd.DataFrame(doc[table_name]) 

    client.close()

    return data


@log_exceptions(
    log,
    f'Data regarding the company {company} successfully deleted from the remote database.',
    f'Unable to delete data regarding the company: {company}.',
    exit_app=True,
    )
def delete_data(
    uri_: str,
    db_name: str,
    collection_name: str,        
    ) -> None:
        client = MongoClient(uri_, server_api=ServerApi('1'))
        db = client[db_name]
        collection = db[collection_name]
        collection.drop()
        client.close()
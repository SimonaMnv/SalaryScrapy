import json

import boto3
from boto3.dynamodb.conditions import Key, Attr

import pandas as pd
from botocore.exceptions import ClientError

from salaryscrape.salaryscrape.utils.secrets_config import config
import logging

if config['ENV'] == 'prod':
    dynamoDB_access_key = config['dynamoDB_access_key']
    dynamoDB_secret_access_key = config["dynamoDB_secret_access_key"]
    api_key = config['positionstack_api_key']
else:
    creds = json.load(open('creds.json'))
    dynamoDB_access_key = creds['dynamodb_access_key']
    dynamoDB_secret_access_key = creds["dynamodb_secret_access_key"]
    api_key = creds["positionstack_api_key"]


class DynamoData:
    def __init__(self):
        self.session = boto3.resource(
            'dynamodb',
            region_name='eu-west-3',
            aws_access_key_id=dynamoDB_access_key,
            aws_secret_access_key=dynamoDB_secret_access_key
        )
        self.tablename = config["remote_db_table_name"]

    def get_dynamodb_data(self, job_title_key=None, date_key=None, job_title_key_val=None,
                          end_date=None, start_date=None):
        """
        Reads data from DynamoDB. First checks if a job and a date range are given to filter out data based on both,
        then checks if nothing is given
        """
        table = self.session.Table(self.tablename)

        try:
            if job_title_key and job_title_key_val and date_key and end_date and start_date:
                dynamodb_data = table.scan(
                    FilterExpression=
                    Attr(job_title_key).eq(job_title_key_val) &
                    Attr(date_key).between(start_date, end_date)
                )
                print(pd.DataFrame.from_dict(dynamodb_data['Items']))
            else:
                dynamodb_data = table.scan()
        except ClientError:
            logging.error("[table_query()] -- Couldn't retrieve data from DynamoDB")
        else:
            return pd.DataFrame.from_dict(dynamodb_data['Items'])

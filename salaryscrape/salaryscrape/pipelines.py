import json
import os

import boto3

from salaryscrape.salaryscrape.utils.secrets_config import config

if config['ENV'] == 'prod':
    dynamoDB_access_key = config['dynamoDB_access_key']
    dynamoDB_secret_access_key = config["dynamoDB_secret_access_key"]
    api_key = config['positionstack_api_key']
else:
    creds = json.load(open(os.path.join(os.pardir, 'creds.json')))
    dynamoDB_access_key = creds['dynamodb_access_key']
    dynamoDB_secret_access_key = creds["dynamodb_secret_access_key"]
    api_key = creds["positionstack_api_key"]


class SalaryscrapePipeline:
    def __init__(self):
        self.session = boto3.resource(
            'dynamodb',
            region_name='eu-west-3',
            aws_access_key_id=dynamoDB_access_key,
            aws_secret_access_key=dynamoDB_secret_access_key
        )
        self.tablename = config["remote_db_table_name"]

    def process_item(self, item, spider):
        """ Write the data to the remote_db_table_name in dynamodb & then add the lat/lot of the location """
        print("Writing item to dynamodb")
        table = self.session.Table(self.tablename)

        table.put_item(
            Item={str(k): str(v) for k, v in item.items()}
        )

        return item

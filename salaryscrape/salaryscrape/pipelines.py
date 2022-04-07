import boto3

from spiders.secrets_config import config


class SalaryscrapePipeline:
    def __init__(self):
        self.session = boto3.resource(
            'dynamodb',
            region_name='eu-west-3',
            aws_access_key_id=config['dynamoDB_access_key'],
            aws_secret_access_key=config["dynamoDB_secret_access_key"]
        )
        self.tablename = config["remote_db_table_name"]

    def process_item(self, item, spider):
        """ write the data to the remote_db_table_name in dynamodb """
        table = self.session.Table(self.tablename)

        table.put_item(
            Item={k: v for k, v in item.items()}
        )

        return item

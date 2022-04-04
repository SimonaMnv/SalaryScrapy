import boto3

from spiders.secrets_config import config


class SalaryscrapePipeline:
    def __init__(self):
        self.session = boto3.Session(region_name='eu-west-3',
                                     aws_access_key_id=config['dynamoDB_access_key'],
                                     aws_secret_access_key=config["dynamoDB_secret_access_key"])
        self.dynamodb = self.session.resource('dynamodb')
        self.tablename = "glassdoor"

    def process_item(self, item, spider):
        """ write the data to dynamodb """
        table = self.dynamodb.Table(self.tablename)
        table.meta.client.get_waiter('table_exists').wait(TableName=self.tablename)

        table.put_item(
            tableName=self.tablename,
            Item={k: v for k, v in item.items()}
        )

        return item

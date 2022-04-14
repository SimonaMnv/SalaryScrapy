import boto3
import requests

from salaryscrape.salaryscrape.utils.secrets_config import config


class SalaryscrapePipeline:
    def __init__(self):
        self.session = boto3.resource(
            'dynamodb',
            region_name='eu-west-3',
            aws_access_key_id=config['dynamoDB_access_key'],
            aws_secret_access_key=config["dynamoDB_secret_access_key"]
        )
        self.tablename = config["remote_db_table_name"]
        self.cords_api = f"http://api.positionstack.com/v1/forward?access_key={config['positionstack_api_key']}&query="

    def process_item(self, item, spider):
        """ Write the data to the remote_db_table_name in dynamodb & then add the lat/lot of the location """
        print("Writing item to dynamodb")
        table = self.session.Table(self.tablename)

        for k, v in item.items():
            # API call to get the lat/lon
            if str(k) == "country":
                r = requests.get(self.cords_api + str(v))
                lat_lon = r.json()
                table.put_item(
                    Item={
                        "lat": lat_lon['data'][0]['latitude'],
                        "lon": lat_lon['data'][0]['longitude']
                    }
                )
            table.put_item(
                Item={
                    str(k): str(v)
                }
            )

        return item

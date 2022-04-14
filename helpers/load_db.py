import json
import os
import unicodedata

import boto3

creds = json.load(open(os.path.join(os.pardir, 'creds.json')))

session = boto3.resource(
    'dynamodb',
    region_name='eu-west-3',
    aws_access_key_id=creds['dynamodb_access_key'],
    aws_secret_access_key=creds["dynamodb_secret_access_key"]
)

with open("worldcities.csv") as f:
    for line in f:
        comma_split = line.split(',')
        country = comma_split[1]
        lat = comma_split[2]
        lon = comma_split[3]
        capital = comma_split[7]

        table = session.Table("lat_lon")

        table.put_item(
            Item={
                "country": country,
                "lat": lat,
                "lon": lon,
                "capital": ''.join(c for c in unicodedata.normalize('NFD', capital)
                                   if unicodedata.category(c) != 'Mn')
            }
        )

        print("writing to dynamodb", {
            "country": country,
            "lat": lat,
            "lon": lon,
            "capital": ''.join(c for c in unicodedata.normalize('NFD', capital)
                               if unicodedata.category(c) != 'Mn')
        })
    f.close()

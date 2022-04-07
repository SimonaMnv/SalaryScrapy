import os

config = {
    "ENV": "dev",
    "glassdoor_username": os.environ.get("GLASSDOOR_USERNAME"),
    "glassdoor_password": os.environ.get("GLASSDOOR_PASSWORD"),
    "dynamoDB_access_key": os.environ.get("DYNAMO_DB_ACCESS_KEY"),
    "dynamoDB_secret_access_key": os.environ.get("DYNAMO_DB_SECRET_ACCESS_KEY"),
    "remote_db_table_name": "glassdoor",
    "root_dir": os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "spider_root_dir": "salaryscrape",
    "spider_name": "glassdoor_spider"
}
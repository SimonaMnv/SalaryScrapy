import os

config = {
    "ENV": "dev",
    "glassdoor_username": os.environ.get("GLASSDOOR_USERNAME"),
    "glassdoor_password": os.environ.get("GLASSDOOR_PASSWORD"),
    "root_dir": os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
}
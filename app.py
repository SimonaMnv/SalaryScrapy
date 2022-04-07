import os

from flask_apscheduler import APScheduler
import datetime
from flask import Flask, jsonify
from salaryscrape.salaryscrape.spiders import secrets_config

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def run_spider():
    os.system(f"cd {secrets_config.config['spider_root_dir']}")
    os.system(f"scrapy crawl {secrets_config.config['spider_name']}")


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=run_spider, trigger='cron', minute='*/1', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

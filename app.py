import crochet

crochet.setup()

import os
from flask_apscheduler import APScheduler
import datetime

from flask import Flask, jsonify
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.signalmanager import dispatcher
from scrapy import signals
from scrapy.utils.project import get_project_settings

from salaryscrape.salaryscrape.spiders import glassdoor_spider

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

crawl_runner = CrawlerRunner(get_project_settings())

output_data = []


def scrape():
    return print("Hi")


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=scrape, trigger='cron', minute='*/2', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

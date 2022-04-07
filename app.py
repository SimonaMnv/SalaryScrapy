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

from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

crawl_runner = CrawlerRunner(get_project_settings())

output_data = []


@crochet.wait_for(timeout=60.0)
def scrape_with_crochet():
    """
    signal fires when single item is processed and calls _crawler_result to append that item
    returns a twisted.internet.defer.Deferred
    """
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(GlassDoor, category="https://www.glassdoor.com/Salaries/")
    print("return eventual")
    return eventual


def _crawler_result(item, response, spider):
    output_data.append(dict(item))
    print(f"{datetime.datetime.now()} Output data crawled:", output_data)


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=scrape_with_crochet, trigger='cron', minute='*/2', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

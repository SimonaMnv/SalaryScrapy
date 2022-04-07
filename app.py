import os

import crochet
from flask_apscheduler import APScheduler
import datetime
from flask import Flask, jsonify

from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor
from salaryscrape.utils.run_spider import GlassdoorScraper

crochet.setup()
app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def scrape_with_crochet():
    scraper = GlassdoorScraper(GlassDoor)
    scraper.run_spider()

    while not scraper.is_closed:
        continue


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=scrape_with_crochet, trigger='cron', minute='*/1', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

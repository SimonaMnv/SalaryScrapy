import crochet
import os
from flask_apscheduler import APScheduler
import datetime
from flask import Flask, jsonify, request
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor
from run_spider import GlassdoorScraper

crochet.setup()
app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

crawl_runner = CrawlerRunner(get_project_settings())
output_data = []


# @app.route('/get_items')
def scrape_with_crochet():
    print("scrape_with_crochet starting")
    scraper = GlassdoorScraper(GlassDoor)
    scraper.run_spider()

    while not scraper.is_closed:
        continue

    return scraper.get_output_data()


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=scrape_with_crochet, trigger='cron', minute='*/2', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

import os
from flask_apscheduler import APScheduler
import datetime

from flask import Flask, jsonify
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from scrapy.utils.project import get_project_settings
from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor


app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def crawl():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(GlassDoor)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return str(datetime.datetime.now()) + '_' + 'Scraping...'


@app.route('/crawl')
def add_tasks():
    app.apscheduler.add_job(func=crawl, trigger='cron', minute='*/5', id='job-crawler')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

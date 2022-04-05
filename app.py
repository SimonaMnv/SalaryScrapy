import os
from flask_apscheduler import APScheduler
import datetime

from flask import Flask, request, jsonify
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from scrapy.utils.project import get_project_settings
from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor


class Config(object):
    JOBS = [
        {
            'id': 'crawl_job',
            'func': '__main__:crawl',
            'trigger': 'cron',
            'day': '1',
            'hour': '6',
            'minute': '0',
            'second': '0'
        },
    ]


app = Flask(__name__)
app.config.from_object(Config())


def crawl():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(GlassDoor)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return 'Scraping...'


@app.route('/')
def index():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/schedule_crawl')
def schedule_crawl():
    scheduler.add_job(id='glassdoor_crawl_job', func=crawl, trigger='interval', minute='2')
    return jsonify({str(datetime.datetime.now()): 'Crawling Scheduled'}), 200


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

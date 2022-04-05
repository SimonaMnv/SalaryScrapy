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
            'day': '*',
            'hour': '6',
            'minute': '0',
            'second': '0'
        },
    ]
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())


def crawl():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(get_project_settings())
    d = runner.crawl(GlassDoor)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return str(datetime.datetime.now()) + '_' + 'Scraping...'


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

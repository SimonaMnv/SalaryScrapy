import os
from flask import Flask, request, abort
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor

app = Flask(__name__)

spiders = ['glassdoor_spider']


@app.route('/')
def index():
    return '200'


@app.route('/crawl', methods=['GET', 'POST'])
def get_data():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner()
    d = runner.crawl(GlassDoor)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return 'Scraping...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

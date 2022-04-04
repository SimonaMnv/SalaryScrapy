import os

from flask import Flask, request, jsonify
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from scrapy.utils.project import get_project_settings
from salaryscrape.salaryscrape.spiders.glassdoor_spider import GlassDoor

app = Flask(__name__)

spiders = ['glassdoor_spider']


@app.route('/')
def index():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/crawl', methods=['GET', 'POST'])
def get_data():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    runner = CrawlerRunner(get_project_settings)
    d = runner.crawl(GlassDoor)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

    return 'Scraping...'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

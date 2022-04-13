import os
from subprocess import call

from flask_apscheduler import APScheduler
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


@app.route('/', methods=['GET'])
def home():
    return jsonify({str(datetime.datetime.now()): ' '}), 200


def run_spider():
    """ run the spider inside the heroku container """
    call(["scrapy", 'crawl', 'glassdoor_spider'], cwd='/app/salaryscrape')


@app.route('/crawl')
def add_tasks():
    """ create a scheduler to execute the spider weekly - one unique id running at a time """
    # TODO: change this @monthly
    app.apscheduler.add_job(func=run_spider, trigger='cron', day_of_week='wed', hour='18', minute='05',
                            id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

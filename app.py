import os
import subprocess

from flask_apscheduler import APScheduler
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def run_spider():
    """ run the spider """
    print("Current dir", subprocess.check_output(['ls'], shell=True))
    subprocess.run(['cd', 'salaryscrape'], shell=True)
    print("Current dir2", subprocess.check_output(['ls'], shell=True))
    subprocess.run(['scrapy', 'crawl', 'glassdoor_spider'], shell=True)


@app.route('/crawl')
def add_tasks():
    """ create a scheduler to execute the spider weekly - one unique id running at a time """
    app.apscheduler.add_job(func=run_spider, trigger='cron', minute='*/1', id='glassdoor_spider_crawl_job')
    return jsonify({str(datetime.datetime.now()): 'crawl job started'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))

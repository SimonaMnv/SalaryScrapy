from flask import jsonify
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapy.utils.project import get_project_settings


class GlassdoorScraper:
    def __init__(self, spider):
        self.output_data = []
        self.is_closed = False
        self.process = CrawlerRunner(get_project_settings())
        self.spider = spider

    def run_spider(self):
        print("run_spider starting")
        dispatcher.connect(self._crawler_result, signal=signals.item_scraped)
        print("dispatcher.connect ended")
        self.process.crawl(self.spider)
        print("process.crawl ended")

    def _crawler_result(self, item, response, spider):
        print("_crawler_result started")
        self.output_data.append(dict(item))
        print("item collected", dict(item))

    def get_output_data(self):
        print("get_output_data starting")
        self.output_data = [dict(t) for t in {tuple(d.items()) for d in self.output_data}]
        return jsonify(self.output_data)

import json
import datetime

import scrapy
from scrapy.spiders.init import InitSpider
from ..items import CompanySalary

import logging
import re

from salaryscrape.salaryscrape.utils.secrets_config import config

JOBS = ["data-engineer-", "data-scientist-", "software-engineer-"]


class GlassDoor(InitSpider):
    name = "glassdoor_spider"
    login_url = 'https://www.glassdoor.com/profile/login_input.htm'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.glassdoor_user = config['glassdoor_username']
        self.glassdoor_pw = config['glassdoor_password']
        self.base_url = "https://www.glassdoor.com/Salaries/"
        self.country_codes = json.load(open(config['root_dir'] + '/salaryscrape/utils/country_codes.json'))

    def init_request(self):
        return scrapy.Request(
            url=self.login_url,
            callback=self.login
        )

    def login(self, response):
        yield scrapy.FormRequest.from_response(
            response=response,
            formid='login_form',
            formdata={
                'username': self.glassdoor_user,
                'password': self.glassdoor_pw,
            },
            callback=self.after_login,
        )

    def after_login(self, response):
        """ authenticate user. check to see if it was successful and if so, init crawling """
        if "authentication failed" or "Please try again" in response.body:
            logging.warning("NOT Authenticated")
            return
        elif "Sign Out" in response.body:
            print("Great! Authenticated")
            logging.warning("Authenticated")
            return self.initialized()

    def start_requests(self):
        """ generate the links """
        for country_k, country_v in self.country_codes.items():
            for job in JOBS:
                final_url = self.base_url + str(country_k).split("_")[1] + job + "salary-SRCH_IL.0,4_IM" + str(country_v) + "_KO" + str(
                    len(str(country_k).split("_")[1])) + "," + str(len(str(country_k).split("_")[1]) + len(job)) + ".htm"
                yield scrapy.Request(url=final_url, callback=self.salary_parse, cb_kwargs={'country':  str(country_k).split("_")[0]})

    @staticmethod
    def salary_parse(response):
        """ clean & parse the data to fetch only what's required """
        salary = CompanySalary()

        main_page = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

        print(f'crawling URL: {response.url}')

        salary['timestamp'] = str(datetime.datetime.now())
        salary['location'] = re.search('(?:.*?\/){4}([^\/-]+)', str(response.url))[1]
        salary['country'] = response.cb_kwargs['country']
        salary['job_title'] = main_page["name"]
        salary['job_percentile10_payment'] = main_page["estimatedSalary"][0]["percentile10"]
        salary['job_median_payment'] = main_page["estimatedSalary"][0]["median"]
        salary['job_percentile90_payment'] = main_page["estimatedSalary"][0]["percentile90"]
        salary['location_currency'] = main_page["estimatedSalary"][0]["currency"]
        salary['sample_size'] = main_page["sampleSize"]
        salary['pay_period'] = re.search('(?<=\/<!-- -->)(.*?)(?=\<)', str(response.xpath('//span[contains(@class, "css-18stkbk")]')[2].extract()))[0]

        print(f'Item crawled: {salary}')

        yield salary

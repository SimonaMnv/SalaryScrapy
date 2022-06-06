import json
import datetime
import os

import requests
import scrapy
from scrapy.spiders.init import InitSpider
from ..items import CompanySalary

import logging
import re

from salaryscrape.salaryscrape.utils.secrets_config import config
from utils.local_payment_to_eur import local_revenue_to_eur


JOBS = ["data-engineer-", "data-scientist-", "software-engineer-"]

if config['ENV'] == 'prod':
    api_key = config['positionstack_api_key']
else:
    creds = json.load(open(os.path.join(os.pardir, 'creds.json')))
    api_key = creds["positionstack_api_key"]


class GlassDoor(InitSpider):
    name = "glassdoor_spider"
    login_url = 'https://www.glassdoor.com/profile/login_input.htm'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.glassdoor_user = config['glassdoor_username']
        self.glassdoor_pw = config['glassdoor_password']
        self.base_url = "https://www.glassdoor.com/Salaries/"
        self.country_codes = json.load(open(config['root_dir'] + '/salaryscrape/utils/country_codes.json'))
        self.cords_api = f"http://api.positionstack.com/v1/forward?access_key={api_key}&query="

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
                final_url = self.base_url + str(country_k).split("_")[1] + job + "salary-SRCH_IL.0,4_IM" + str(
                    country_v) + "_KO" + str(
                    len(str(country_k).split("_")[1])) + "," + str(
                    len(str(country_k).split("_")[1]) + len(job)) + ".htm"
                yield scrapy.Request(url=final_url, callback=self.salary_parse,
                                     meta={'country': str(country_k).split("_")[0]})

    def salary_parse(self, response):
        """
        clean & parse the data to fetch only what's required.
        also, get the lat & lon based on the country.
        also, transform the country's local currency to euro so they all have the same currency type
        """
        salary = CompanySalary()

        main_page = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

        r = requests.get(self.cords_api + response.meta['country'])
        lat_lon = r.json()

        local_currency_to_eur = local_revenue_to_eur(
            main_page["estimatedSalary"][0]["currency"],
            main_page["estimatedSalary"][0]["median"],
            str(datetime.datetime.today().strftime('%Y-%m-%d'))
        )

        print(f'crawling URL: {response.url}')

        salary['timestamp'] = str(datetime.datetime.now())
        salary['updated_at'] = str(datetime.datetime.today().strftime('%Y-%m-%d'))
        salary['location'] = re.search('(?:.*?\/){4}([^\/-]+)', str(response.url))[1]
        salary['country'] = response.meta['country']
        salary['lat'] = lat_lon['data'][0]['latitude']
        salary['lon'] = lat_lon['data'][0]['longitude']
        salary['job_title'] = main_page["name"]
        salary['job_percentile10_payment'] = main_page["estimatedSalary"][0]["percentile10"]
        salary['job_median_payment'] = main_page["estimatedSalary"][0]["median"]
        salary['job_percentile90_payment'] = main_page["estimatedSalary"][0]["percentile90"]
        salary['location_currency'] = main_page["estimatedSalary"][0]["currency"]
        salary['job_median_to_eur'] = str(local_currency_to_eur)
        salary['sample_size'] = main_page["sampleSize"]
        salary['pay_period'] = re.search('(?<=\/<!-- -->)(.*?)(?=\<)',
                                         str(response.xpath('//span[contains(@class, "css-18stkbk")]')[2].extract()))[0]

        print(f'Item crawled: {salary}')

        yield salary

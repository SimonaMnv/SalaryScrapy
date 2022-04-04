import json
import datetime

import scrapy
from scrapy.spiders.init import InitSpider
from ..items import CompanySalary

import logging

from .secrets_config import config


class GlassDoor(InitSpider):
    name = "glassdoor_salary"
    login_url = 'https://www.glassdoor.com/profile/login_input.htm'

    def __init__(self):
        self.glassdoor_user = config['glassdoor_username']
        self.glassdoor_pw = config['glassdoor_password']
        self.base_url = "https://www.glassdoor.com/Salaries/"

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
        eu_countries = json.load(open(config['root_dir'] + '/static_files/eu_countries.json'))
        jobs = json.load(open(config['root_dir'] + '/static_files/jobs.json'))

        for country_k, country_v in eu_countries.items():
            for job_k, job_v in jobs.items():
                final_url = self.base_url + country_k + job_v + country_v + str(len(job_v) + len(country_k)) + ".htm"
                yield scrapy.Request(url=final_url, callback=self.salary_parse)

    @staticmethod
    def salary_parse(response):
        """ clean & parse the data to fetch only what's required """
        salary = CompanySalary()

        main_page = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())

        salary['timestamp'] = str(datetime.datetime.now())
        salary['location'] = main_page["occupationLocation"][0]["name"]
        salary['job_title'] = main_page["name"]
        salary['job_percentile10_payment'] = main_page["estimatedSalary"][0]["percentile10"]
        salary['job_median_payment'] = main_page["estimatedSalary"][0]["median"]
        salary['job_percentile90_payment'] = main_page["estimatedSalary"][0]["percentile90"]
        salary['location_currency'] = main_page["estimatedSalary"][0]["currency"]
        salary['sample_size'] = main_page["sampleSize"]

        yield salary
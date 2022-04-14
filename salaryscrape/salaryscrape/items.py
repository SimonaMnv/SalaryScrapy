# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanySalary(scrapy.Item):
    timestamp = scrapy.Field()
    location = scrapy.Field()
    country = scrapy.Field()
    job_title = scrapy.Field()
    job_percentile10_payment = scrapy.Field()
    job_median_payment = scrapy.Field()
    job_percentile90_payment = scrapy.Field()
    location_currency = scrapy.Field()
    sample_size = scrapy.Field()
    pay_period = scrapy.Field()
    # highest_paying_companies = scrapy.Field() # todo: add this

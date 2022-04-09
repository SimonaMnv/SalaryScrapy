# Salary Scrapy 
This project crawls through Glassdoor and analyzes the salaries per profession and country.
The proffession is simply declared in the ```glassdoor_spider.py``` in an array and the countries 
are located in ```utils/country_codes.json```. More can be added in both

# Crawler
The first part is the crawler. The salaryscraper crawls through specific urls to download the data as seen below:

``` 
{
     'country_currency': 'EUR',
     'job_median_payment': '1298',
     'job_percentile10_payment': '869',
     'job_percentile90_payment': '2434',
     'job_title': 'Data Scientist',
     'location': 'Athens, Attica',
     'sample_size': '56'
 }
 ```

# DynamoDB
This project uses a connection to AWS DynamoDB to store the data in.
   1. Create a new table called "glassdoor" in DynamoDB and create & set partition key to "timestamp"
   2. Go in IAM and create a new User group and under attach permissions policies use only "AmazonDynamoDBFullAccess" 
   also create a user and add him to that group
   3. The above steps will also give you the Access key ID & Secret key access that is needed in order to host this in Heroku
   add those in environment variables in Heroku and also add in your glassdoor username & password to authenticate the session
   4. The pipeline that stores the data in herokuDB along with the connection initialization is in `pipelines.py`

# Scrapy & Heroku & Flask 
   - The ```glassdoor_spider``` scrapes the data by creating the URLs based on the information in the static_files
   - Scraping in Heroku is not allowed so proxies should be used instead (`salaryscrape/settings.py`) and that makes the process slower
   to make this faster, hit an API with valid proxies instead of a static list
   - The ```pipelines.py``` store each parsed item into the dynamodb table

# Scheduler
   - When we post a request at ```/crawl```, the spider is triggered and then the scheduler takes over to keep triggering it 
   - The crawling is scheduled once every 2 weeks to get up-to-date date plus gather historical data

# How to run
 - To run locally simply change ```SPIDER_MODULES``` & ```NEWSPIDER_MODULE``` & ```ITEM_PIPELINES``` in ```settings.py``` to ```salaryscrape.spiders```
 and the same for ```default``` in ```scrapy.cfg```. Then run ```scrapy crawl glassdoor_spider``` while in the scrapy dir
 - To run in heroku, simply deploy it and run once the `````/crawl````` endpoint. Make sure to have all env variables as described above
 - More jobs/countries can be added in 

# TODO: 
1. Add in Streamlit UI
2. Unit tests 
3. Add circleci for 1) linting 2) black lib 3) unit tests
import pytz
import requests
import subprocess
from apscheduler.schedulers.twisted import TwistedScheduler
from twisted.internet import reactor


def send_request():
    requests.post(
        "https://salaryscrape.herokuapp.com/schedule.json", data={
            "project": "salaryscrape",
            "spider": "glassdoor_spider"
        })


if __name__ == "__main__":
    """ start the crawler every monday at 6 AM UTC time """

    subprocess.run("scrapyd-deploy", shell=True, universal_newlines=True)

    scheduler = TwistedScheduler(timezone=pytz.timezone('UTC'))
    scheduler.add_job(send_request, 'cron', day_of_week='monday', hour=6, minute=0)
    scheduler.start()

    reactor.run()

import unittest

import requests

from salaryscrape.utils.local_payment_to_eur import local_revenue_to_eur
from salaryscrape.salaryscrape.utils.secrets_config import config


class CheckExternalAPIs(unittest.TestCase):
    def setUp(self):
        self.cords_api = f"http://api.positionstack.com/v1/forward?access_key={config['positionstack_api_key']}&query="
        print("setUp is running")

    def test_currency_api(self):
        """ check that the https://api.exchangerate.host is available. this converts 1 eur to eur """
        api_status = local_revenue_to_eur('eur', '1', '2022-06-07')
        self.assertTrue(api_status == 1)

    def test_lat_lon_api(self):
        """ check that the api lat/lon api is available. check that greece's lat is 39.78331"""
        r = requests.get(self.cords_api + 'greece')
        lat_lon = r.json()
        self.assertTrue(lat_lon['data'][0]['latitude'] == '39.78331')

    def tearDown(self) -> None:
        """ bye bye """
        print("tearDown is running")

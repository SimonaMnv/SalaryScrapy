import requests


def local_revenue_to_usd(local_currency, local_price, date):
    """
    Convert local currency to EUR. No API key needed.
    Example: https://api.exchangerate.host/convert?from=RUB&to=EUR&date=2022-05-02&amount=1000
    """
    url = 'https://api.exchangerate.host/convert?from={lc}&to=EUR&date={dt}&amount={lp}'.format(
        lc=local_currency, lp=local_price, dt=date)

    response = requests.get(url)
    data = response.json()

    return data['result']

import requests


def get_proxies(proxy_endpoint):
    r = requests.get(proxy_endpoint)
    proxies = r.text.split("\n")
    proxies = [x for x in proxies if x]
    print("Proxies:", proxies)
    return proxies


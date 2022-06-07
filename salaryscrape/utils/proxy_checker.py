import requests
# import multiprocessing

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive",
}


def getproxies():
    resp = requests.get(
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1500&country=all&ssl=all&anonymity"
        "=all"
    )
    resp.raise_for_status()
    return set(filter(None, resp.text.splitlines()))


def check_proxy(proxy_addr: str):
    good_proxies = set()

    for proxy in proxy_addr:
        try:
            runner = f"http://{proxy}"
            res = requests.get(
                "https://api.ipify.org?format=json",
                proxies={"http": runner, "https": runner},
                headers=headers,
                timeout=1.5,
            )
            res.raise_for_status()
            good_proxies.add(proxy)
        except Exception:
            pass

    return good_proxies

# if __name__ == "__main__":
#     good_proxies = set()
#     proxies = getproxies()
#     with multiprocessing.Pool() as p:
#         for proxy_addr, result in p.imap_unordered(check_proxy, proxies, chunksize=8):
#             if result:
#                 good_proxies.add(proxy_addr)

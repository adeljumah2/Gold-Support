import requests
from pyquery import PyQuery as pq
from concurrent.futures import ThreadPoolExecutor

urls = {
    "gold": "https://www.investing.com/commodities/gold-historical-data",
    "silver": "https://www.investing.com/commodities/silver-historical-data"
}

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_data(name, url):
    response = requests.get(url, headers=headers)
    doc = pq(response.text)
    table = pq(doc("table")[1])
    row = table("tr")[1]
    cols = pq(row)("td")

    return {
        "commodity": name,
        "date": pq(cols[0]).text(),
        "price": pq(cols[1]).text()
    }

results = []

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(fetch_data, k, v) for k, v in urls.items()]
    for f in futures:
        results.append(f.result())

print(results)

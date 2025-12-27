from pyquery import PyQuery as pq
import requests
import json

url = "https://www.investing.com/commodities/gold-historical-data"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

doc = pq(response.text)

table_index = 1
table = pq(doc("table")[table_index])

rows = table("tr")

gold_data = []

for row in rows[1:]:  
    cols = pq(row)("td")
    if len(cols) >= 2:
        date = pq(cols[0]).text()
        price = pq(cols[1]).text()

        gold_data.append({
            "date": date,
            "price": price
        })

print(f"Collected {len(gold_data)} rows")
print(gold_data[:5]) 


with open("data/raw_gold_prices.json", "w", encoding="utf-8") as f:
    json.dump(gold_data, f, indent=4)

print("Data saved to data/raw_gold_prices.json")

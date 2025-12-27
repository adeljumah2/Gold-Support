import pandas as pd
import json
from sklearn.preprocessing import MinMaxScaler

df = pd.read_json("data/raw_gold_prices.json")

df["price"] = (
    df["price"]
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["date"] = pd.to_datetime(df["date"])

scaler = MinMaxScaler()
df["normalized_price"] = scaler.fit_transform(df[["price"]])

min_price = df["price"].min()
max_price = df["price"].max()
avg_price = df["price"].mean()

latest_price = df.sort_values("date", ascending=False).iloc[0]["price"]

if latest_price < avg_price:
    signal = "Potential Buy Signal"
else:
    signal = "Potential Sell Signal"

best_buy_days = (
    df[df["price"] < avg_price]
    .sort_values("price")
    .head(3)[["date", "price"]]
)

best_sell_days = (
    df[df["price"] > avg_price]
    .sort_values("price", ascending=False)
    .head(3)[["date", "price"]]
)

results = {
    "min_price": round(float(min_price), 2),
    "max_price": round(float(max_price), 2),
    "average_price": round(float(avg_price), 2),
    "latest_price": round(float(latest_price), 2),
    "signal": signal,
    "best_buy_days": best_buy_days.to_dict(orient="records"),
    "best_sell_days": best_sell_days.to_dict(orient="records")
}

with open("data/analysis_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, default=str)

print("Analysis results saved successfully.")

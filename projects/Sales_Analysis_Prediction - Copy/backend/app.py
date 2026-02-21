import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load only ML models (usually smaller than full dataset)
sales = joblib.load(os.path.join(BASE_DIR, "sales.pkl"))
demand = joblib.load(os.path.join(BASE_DIR, "demand.pkl"))
profit = joblib.load(os.path.join(BASE_DIR, "profit.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# Lazy cache
_rules = None
_df = None

def get_rules():
    global _rules
    if _rules is None:
        _rules = pd.read_csv(os.path.join(BASE_DIR, "rules.csv"))
    return _rules

def get_df():
    global _df
    if _df is None:
        # OPTIONAL: load only needed columns to save memory
        usecols = ["Sales", "Profit", "Customer ID", "Month", "Region"]
        _df = pd.read_csv(os.path.join(BASE_DIR, "engineered_data.csv"), usecols=usecols)
    return _df

@app.route("/")
def home():
    return {"status": "AI Sales System Running"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    X = np.array([[data["profit"], data["discount"], data["quantity"], data["year"], data["month"],
                   data["is_weekend"], data["customer_orders"], data["product_demand"]]])
    X = scaler.transform(X)
    return jsonify({
        "sales": float(sales.predict(X)[0]),
        "demand": float(demand.predict(X)[0]),
        "profit": float(profit.predict(X)[0])
    })

@app.route("/analytics")
def analytics():
    df = get_df()
    return jsonify({
        "total_sales": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "customers": int(df["Customer ID"].nunique()),
        "monthly_sales": df.groupby("Month")["Sales"].sum().to_dict(),
        "region_sales": df.groupby("Region")["Sales"].sum().to_dict()
    })

@app.route("/recommend")
def recommend():
    rules = get_rules()
    recs = rules.sort_values("lift", ascending=False).head(10)
    cleaned = []
    for _, row in recs.iterrows():
        cleaned.append({
            "buy": list(eval(row["antecedents"])),
            "recommend": list(eval(row["consequents"])),
            "confidence": round(row["confidence"], 2),
            "lift": round(row["lift"], 2),
            "support": round(row["support"], 4)
        })
    return jsonify(cleaned)

@app.route("/bundles")
def bundles():
    rules = get_rules()
    recs = rules.sort_values("lift", ascending=False).head(5)
    bundles = []
    for _, row in recs.iterrows():
        bundles.append({
            "bundle": list(eval(row["antecedents"])) + list(eval(row["consequents"])),
            "confidence": round(row["confidence"], 2),
            "lift": round(row["lift"], 2)
        })
    return jsonify(bundles)

@app.route("/stock-alert")
def stock_alert():
    rules = get_rules()
    top = rules.sort_values("confidence", ascending=False).head(5)
    alerts = []
    for _, row in top.iterrows():
        products = list(eval(row["consequents"]))
        alerts.append({
            "products": products,
            "message": "High demand expected – Increase stock",
            "confidence": round(row["confidence"], 2),
            "lift": round(row["lift"], 2)
        })
    return jsonify(alerts)

if __name__ == "__main__":
    app.run(debug=True)



import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

from advisor import generate_insights

app = Flask(__name__)

CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sales = joblib.load(os.path.join(BASE_DIR, "sales.pkl"))
demand = joblib.load(os.path.join(BASE_DIR, "demand.pkl"))
profit = joblib.load(os.path.join(BASE_DIR, "profit.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

rules = pd.read_csv(os.path.join(BASE_DIR, "rules.csv"))
df = pd.read_csv(os.path.join(BASE_DIR, "engineered_data.csv"))

@app.route("/")
def home():
    return {"status":"AI Sales System Running"}



@app.route("/predict",methods=["POST"])
def predict():

    data = request.json

    X = np.array([[

        data["profit"],
        data["discount"],
        data["quantity"],
        data["year"],
        data["month"],
        data["is_weekend"],
        data["customer_orders"],
        data["product_demand"]

    ]])

    X = scaler.transform(X)

    return jsonify({

        "sales": float(sales.predict(X)[0]),
        "demand": float(demand.predict(X)[0]),
        "profit": float(profit.predict(X)[0])

    })


# Analytics
@app.route("/analytics")
def analytics():

    return jsonify({

        "total_sales": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "customers": int(df["Customer ID"].nunique()),

        "monthly_sales": df.groupby("Month")["Sales"].sum().to_dict(),

        "region_sales": df.groupby("Region")["Sales"].sum().to_dict()

    })


# Recommendations
@app.route("/recommend")
def recommend():

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

# AI Advisor
@app.route("/advisor")
def advisor():

    tips = generate_insights()

    return {"insights":tips}

@app.route("/bundles")
def bundles():

    recs = rules.sort_values("lift", ascending=False).head(5)

    bundles = []

    for _, row in recs.iterrows():

        bundles.append({
            "bundle": list(eval(row["antecedents"])) + list(eval(row["consequents"])),
            "confidence": round(row["confidence"],2),
            "lift": round(row["lift"],2)
        })

    return jsonify(bundles)
@app.route("/stock-alert")
def stock_alert():

    # Top rules by confidence
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

if __name__=="__main__":
    app.run(debug=True)

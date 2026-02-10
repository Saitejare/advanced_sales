import pandas as pd

df = pd.read_csv(r"B:\projects\Sales_Analysis_Prediction - Copy\backend\engineered_data.csv")

def generate_insights():

    insights = []

    weekend = df.groupby("Is_Weekend")["Sales"].mean()

    if weekend[1] > weekend[0]:
        insights.append("Increase weekend inventory")

    profit_margin = (df["Profit"].sum()/df["Sales"].sum())*100

    if profit_margin < 15:
        insights.append("Reduce discount offers")

    avg_order = df["Sales"].mean()

    if avg_order < 250:
        insights.append("Introduce bundle offers")

    return insights

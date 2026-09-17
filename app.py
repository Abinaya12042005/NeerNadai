"""
app.py
-------
Main Flask web app. Rendrendu run pannunga: python app.py
Then open: http://127.0.0.1:5000

Routes:
  /                -> dashboard page (area-wise wastage + charts + chatbot widget)
  /api/dashboard    -> JSON data for the charts (reads live from CSV, so if you
                       replace the CSV with fresh data, dashboard updates
                       automatically - this is what makes it "real-time")
  /api/chat  (POST) -> RAG chatbot endpoint, used by the chat widget JS
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import joblib
import os

import rag_chatbot

app = Flask(__name__)

DATA_PATH = "data/area_wise_consumption.csv"
MODEL_PATH = "model/wastage_model.pkl"
ENCODER_PATH = "model/area_encoder.pkl"


def load_model():
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        return model, encoder
    return None, None


model, area_encoder = load_model()


def get_dashboard_data():
    """Reads the CSV fresh on every call - so any update to the data file
    (e.g. a cron job pulling new numbers) shows up on refresh without
    restarting the server."""
    df = pd.read_csv(DATA_PATH)
    df["Date_parsed"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    latest_date = df["Date_parsed"].max()
    recent = df[df["Date_parsed"] >= latest_date - pd.Timedelta(days=30)]

    area_summary = []
    for area, group in recent.groupby("Area"):
        avg_lpcd = group["Actual_LPCD"].mean()
        avg_wastage = group["Wastage_LPCD"].mean()
        pop = int(group["Population_Served"].iloc[0])

        risk = "Unknown"
        if model is not None:
            row = group.iloc[-1]
            month = row["Date_parsed"].month
            dow = row["Date_parsed"].dayofweek
            area_code = area_encoder.transform([area])[0]
            X = pd.DataFrame(
                [[area_code, pop, row["Actual_LPCD"], month, dow]],
                columns=["Area_Code", "Population_Served", "Actual_LPCD", "Month", "DayOfWeek"],
            )
            risk = model.predict(X)[0]

        area_summary.append({
            "area": area,
            "population": pop,
            "avg_lpcd": round(avg_lpcd, 1),
            "avg_wastage_lpcd": round(avg_wastage, 1),
            "risk": risk,
        })

    # Trend line data (last 60 days, city-wide average)
    trend = df.sort_values("Date_parsed").tail(60 * 4)  # 4 areas x 60 days
    trend_by_date = trend.groupby("Date_parsed")["Actual_LPCD"].mean().reset_index()
    trend_data = {
        "labels": trend_by_date["Date_parsed"].dt.strftime("%d %b").tolist(),
        "values": trend_by_date["Actual_LPCD"].round(1).tolist(),
    }

    return {
        "areas": area_summary,
        "trend": trend_data,
        "last_updated": latest_date.strftime("%d %b %Y"),
    }


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/dashboard")
def api_dashboard():
    return jsonify(get_dashboard_data())


@app.route("/api/chat", methods=["POST"])
def api_chat():
    user_msg = request.json.get("message", "")
    if not user_msg.strip():
        return jsonify({"reply": "Kekunga oru question! (Please ask a question.)"})
    reply = rag_chatbot.answer_query(user_msg)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    # Build the RAG index once at startup so the first chat message is fast
    rag_chatbot.build_index()
    app.run(debug=True, host="0.0.0.0", port=5000)

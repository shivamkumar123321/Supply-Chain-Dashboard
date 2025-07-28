import os
import requests
import datetime
from flask import Flask, request
import openai
from algolia_utils import push_records

# Load your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mock warehouse endpoints
WAREHOUSE_APIS = {
    "A": os.getenv("WAREHOUSE_A_API"),
    "B": os.getenv("WAREHOUSE_B_API")
}

def fetch_and_enrich():
    now = datetime.datetime.utcnow()
    enriched = []

    for wh, url in WAREHOUSE_APIS.items():
        resp = requests.get(url)
        resp.raise_for_status()

        for rec in resp.json():
            # 1) Compute delay and status
            exp = datetime.datetime.fromisoformat(rec["expectedDeliveryDate"])
            delay = (now - exp).days
            status = "on-time" if delay <= 0 else ("delayed" if delay < 5 else "critical")

            # 2) AI‑powered risk summary
            prompt = f"Summarize shipment risk: {rec}"
            ai_resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            risk = ai_resp.choices[0].message.content.strip()

            # 3) Reverse‑geocode origin → region bucket
            lat = rec.get("originLat")
            lng = rec.get("originLng")
            geo = requests.get(
                f"https://api.bigdatacloud.net/data/reverse-geocode-client"
                f"?latitude={lat}&longitude={lng}&localityLanguage=en"
            ).json()
            country = geo.get("countryCode", "")
            if country in ["FR", "DE", "GB", "IT"]:
                region = "EMEA"
            elif country in ["CN", "JP", "IN"]:
                region = "APAC"
            else:
                region = "AMERICAS"

            # 4) Build enriched record
            enriched.append({
                **rec,
                "warehouse": wh,
                "delayDays": max(delay, 0),
                "delayStatus": status,
                "riskSummary": risk,
                "region": region,
                "lastUpdated": now.isoformat()
            })

    # Push all to Algolia
    push_records(enriched)
    print(f"[{now.isoformat()}] Pushed {len(enriched)} enriched records")

# Expose as a webhook endpoint for n8n (or any event source)
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def on_update():
    fetch_and_enrich()
    return "OK", 200

@app.route("/", methods=["GET"])
def health():
    return "✅ Ingestion service up", 200


if __name__ == "__main__":
    # For local testing
    app.run(host="0.0.0.0", port=8080)


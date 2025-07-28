import os, requests
import pandas as pd
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Supply‑Chain Dashboard", layout="wide")
st.title("📦 Supply‑Chain Query Dashboard")

query = st.text_input("Enter your query (e.g. “delayed over 2 days from A”):")
facets_wh = st.multiselect("🏭 Warehouse", ["A", "B"])
facets_status = st.multiselect("⚠️ Status", ["on-time", "delayed", "critical"])
delay_slider = st.slider("⏱ Minimum delay days", 0, 30, 0)

if st.button("Search"):
    payload = {
        "query": query or "",
        "facetFilters": [],
        "numericFilters": [f"delayDays>={delay_slider}"]
    }

    if facets_wh:
        payload["facetFilters"].append([f"warehouse:{w}" for w in facets_wh])
    if facets_status:
        payload["facetFilters"].append([f"delayStatus:{s}" for s in facets_status])

    try:
        r = requests.post("http://localhost:5000/search", json=payload, timeout=10)
        r.raise_for_status()
        hits = r.json().get("hits", [])
    except Exception as e:
        st.error(f"Search error: {e}")
        hits = []

    if hits:
        df = pd.DataFrame(hits)
        if "lastUpdated" in df.columns:
            last_update = df["lastUpdated"].max()
            if last_update:
                ts = datetime.fromisoformat(last_update).strftime('%Y-%m-%d %H:%M:%S')
                st.caption(f"Last updated: {ts} UTC")

        # Add emoji badges for status
        def badge(status):
            return f"🟢 {status}" if status == "on-time" else (f"🟡 {status}" if status == "delayed" else f"🔴 {status}")

        df["Status"] = df["delayStatus"].apply(badge)

        display_cols = {
            "shipmentId": "Shipment ID",
            "origin": "Origin",
            "destination": "Destination",
            "delayDays": "Delay (days)",
            "Status": "Status",
        }

        st.dataframe(df[list(display_cols.keys())].rename(columns=display_cols), use_container_width=True)

        # --- Map view of origins ---
        if "originLat" in df.columns and "originLng" in df.columns:
            map_df = df.rename(columns={"originLat": "lat", "originLng": "lon"})
            st.subheader("📍 Shipment Origin Map")
            st.map(map_df[["lat", "lon"]])

    else:
        st.warning("No results found.")

# Footer UX tip
st.markdown("---")
st.info("💡 Try queries like: 'critical shipments to Asia' or 'late shipments from warehouse B over 5 days'.")

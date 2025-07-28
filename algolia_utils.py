# streamlit_app.py
import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime

# --- Config ---
# Point to your MCP proxy endpoint (default port of mcp_proxy.py is 5000)
PROXY_URL = os.getenv("MCP_PROXY_URL", "http://localhost:5000/search")

# --- UI Setup ---
st.set_page_config(page_title="Supply‑Chain Dashboard", layout="wide")
st.title("📦 Supply‑Chain Query Dashboard")

# --- Input Controls ---
query = st.text_input("🔎 Enter your query (e.g., 'delayed over 2 days from A'):")
facets_wh = st.multiselect("🏭 Warehouse", ["A", "B"])
facets_status = st.multiselect("⚠️ Status", ["on-time", "delayed", "critical"])
delay_slider = st.slider("⏱ Minimum delay days", 0, 30, 0)

# Search button
enable_search = st.button("Search")

# --- Search & Display ---
if enable_search:
    # Build payload
    payload = {
        "query": query or "",
        "facetFilters": [],
        "numericFilters": [f"delayDays>={delay_slider}"]
    }
    if facets_wh:
        payload["facetFilters"].append([f"warehouse:{w}" for w in facets_wh])
    if facets_status:
        payload["facetFilters"].append([f"delayStatus:{s}" for s in facets_status])

    # Perform search
    try:
        resp = requests.post(PROXY_URL, json=payload, timeout=10)
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
    except Exception as e:
        st.error(f"Search error: {e}")
        hits = []

    # Handle results
    if not hits:
        st.write("No results found.")
    else:
        df = pd.DataFrame(hits)
        # Display last updated timestamp
        last_update = df.get("lastUpdated").max()
        if last_update:
            ts = datetime.fromisoformat(last_update).strftime('%Y-%m-%d %H:%M:%S')
            st.caption(f"Last updated: {ts} UTC")

        # Add status badge column
        def badge(status):
            return f"🟢 {status}" if status == "on-time" else (f"🟡 {status}" if status == "delayed" else f"🔴 {status}")
        df["Status"] = df["delayStatus"].apply(badge)

        # Select and rename columns
        display_cols = {
            "shipmentId": "Shipment ID",
            "origin": "Origin",
            "destination": "Destination",
            "delayDays": "Delay (days)",
            "Status": "Status"
        }
        st.dataframe(df[list(display_cols.keys())].rename(columns=display_cols), use_container_width=True)

# Footer tip
st.markdown("---")
st.info("Tip: Try queries like 'critical shipments to EMEA region' or 'late shipments from B over 5 days'.")






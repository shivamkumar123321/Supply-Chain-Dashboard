# Supply‑Chain Query Dashboard

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials.
2. `docker-compose up --build`

## Services

- **Ingestion** (`ingestion.py`): fetches & enriches data every minute.
- **MCP Proxy** (`mcp_proxy.py`): translates NL queries via your MCP Server.
- **Frontend** (`streamlit_app.py`): user interface on port 8501.

## Usage

- Open http://localhost:8501  
- Type “show me all shipments delayed over 2 days from A” and hit Search.

Good luck—and may your submission clear that \$1,000 hurdle!
::contentReference[oaicite:0]{index=0}

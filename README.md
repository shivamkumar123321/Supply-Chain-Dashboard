# Supply-Chain Query Dashboard

This project is a Streamlit-based dashboard for querying supply-chain shipment data. It features a sophisticated data ingestion pipeline that enriches shipment data with real-time delay calculations, AI-powered risk summaries from OpenAI, and geographic region bucketing.

## Features

*   **Interactive Dashboard**: A user-friendly web interface built with Streamlit to filter and search for shipment data.
*   **Data Ingestion**: A service that fetches data from multiple warehouse APIs.
*   **Data Enrichment**:
    *   **Delay Calculation**: Automatically calculates the delay in days for each shipment.
    *   **AI-Powered Risk Analysis**: Uses the OpenAI API (gpt-4o-mini) to generate a natural language summary of the risks associated with each shipment.
    *   **Geolocation**: Reverse-geocodes shipment origins to categorize them into regions (EMEA, APAC, AMERICAS).
*   **Search Backend**: Uses Algolia to provide a fast and powerful search experience.
*   **Containerized**: The entire application is containerized using Docker for easy setup and deployment.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a `.env` file**
    Copy the `.env.example` file to a new file named `.env`.
    ```sh
    cp .env.example .env
    ```
    Open the `.env` file and fill in your credentials for Algolia, OpenAI, and the warehouse APIs.

3.  **Build and run the application**
    ```sh
    docker-compose up --build
    ```
    This will build the Docker images and start the `frontend`, `ingestion`, and `mcp_proxy` services.

4.  **Access the application**
    Open your web browser and navigate to `http://localhost:8501`.

## Services

The application is composed of three main services:

*   **`frontend`**: The Streamlit web application that you interact with in your browser. It runs on port 8501.
*   **`ingestion`**: This service is responsible for fetching the raw shipment data from the warehouse APIs, enriching it with additional information, and then pushing it to your Algolia index.
*   **`mcp_proxy`**: This is a Flask-based proxy that sits between the frontend and the search backend. The frontend sends search queries to this proxy.

## Important Note: `mcp_proxy.py`

The `mcp_proxy.py` file in this repository is a placeholder and does **not** contain the final logic to handle the search queries. You will need to implement the logic to translate the incoming requests from the frontend into Algolia search queries. The current implementation simply returns the received data.

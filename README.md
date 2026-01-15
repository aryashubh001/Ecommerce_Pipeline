# Ecommerce_Pipeline
# Real-Time E-Commerce Analytics Pipeline 🚀

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?style=for-the-badge&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-Visualization-FF4B4B?style=for-the-badge&logo=streamlit)

## 📌 Project Overview
This project is a **End-to-End Data Engineering Pipeline** designed to ingest, process, and visualize high-volume e-commerce clickstream data in real-time. 

Built to simulate a production-grade data environment, the system handles "messy" raw data (simulating real-world anomalies), performs automated **ETL (Extract, Transform, Load)** operations, and serves actionable insights via a live interactive dashboard.

## 🏗️ Architecture
The pipeline follows a Producer-Consumer architecture:

1.  **Data Ingestion (Producer):** Generates synthetic user logs (Clicks, Cart Adds, Purchases) with intentional anomalies (null users, negative prices) to simulate production noise.
2.  **Data Storage (Raw Layer):** Buffers raw, unstructured JSON logs into a persistent store (SQLite).
3.  **ETL Engine (Processing Layer):** * **Extracts** raw data.
    * **Transforms** JSON blobs into structured relational tables.
    * **Cleans** data by enforcing schema validation (removing nulls and invalid transactions).
    * **Loads** clean data into an analytics-ready table.
4.  **Visualization (Presentation Layer):** A Streamlit dashboard that polls the clean data store to render real-time KPIs and trend charts.

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas (DataFrames, Vectorized operations)
* **Database:** SQLite (Persistent logging)
* **Visualization:** Streamlit, Plotly Express
* **Simulation:** Faker Library (Synthetic data generation)

## ⚡ Key Features
* **Automated Data Wrangling:** The ETL script automatically detects and quarantines corrupt records (e.g., missing User IDs), ensuring data integrity for downstream analysis.
* **Real-Time Observability:** The dashboard updates automatically, providing live monitoring of "Revenue per Second" and "Traffic Spikes."
* **Scalable Design Pattern:** Decoupled architecture (Producer separate from Consumer) allows for independent scaling of ingestion and processing layers.

## 🚀 How to Run locally
This simulation requires three terminal windows running concurrently.

Here is the text from the image formatted with individual code blocks for each section:

### 🚀 How to Run locally

This simulation requires three terminal windows running concurrently.

**1. Install Dependencies**

```bash
pip install pandas faker streamlit plotly

```

**2. Start the Data Producer (Terminal 1)**
Generates fake user traffic.

```bash
python producer.py

```

**3. Start the ETL Engine (Terminal 2)**
Cleans and processes data every 10 seconds.

```bash
python etl.py

```

**4. Launch the Dashboard (Terminal 3)**
Opens the web interface.

```bash
python -m streamlit run dashboard.py

```

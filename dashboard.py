import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import time

# Page Config
st.set_page_config(page_title="Real-Time Analytics", layout="wide")
st.title("📊 Real-Time E-Commerce Dashboard")

# Function to fetch data
def get_data():
    conn = sqlite3.connect('ecommerce.db')
    # We only read from the CLEAN table, not the raw one
    try:
        df = pd.read_sql("SELECT * FROM clean_data", conn)
        conn.close()
        return df
    except:
        conn.close()
        return pd.DataFrame()

# Auto-refresh logic
placeholder = st.empty()

while True:
    df = get_data()
    
    with placeholder.container():
        if df.empty:
            st.warning("Waiting for data... (Run producer.py and etl.py!)")
        else:
            # KPIS
            total_sales = df[df['event_type'] == 'purchase']['price'].sum()
            total_events = len(df)
            
            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Revenue", f"${total_sales:,.2f}")
            kpi2.metric("Total Events", total_events)
            # Safe handling of timestamp for the KPI
            latest_time = pd.to_datetime(df['timestamp']).max().strftime('%H:%M:%S')
            kpi3.metric("Latest Event Time", latest_time)

            # CHARTS
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Revenue by Product")
                sales_by_product = df[df['event_type'] == 'purchase'].groupby('product')['price'].sum().reset_index()
                if not sales_by_product.empty:
                    fig_bar = px.bar(sales_by_product, x='product', y='price', color='product')
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No sales data yet.")
                
            with col2:
                st.subheader("Traffic Activity")
                event_counts = df['event_type'].value_counts().reset_index()
                event_counts.columns = ['Event Type', 'Count']
                fig_pie = px.pie(event_counts, values='Count', names='Event Type')
                st.plotly_chart(fig_pie, use_container_width=True)

            st.subheader("Latest Clean Transactions")
            st.dataframe(df.tail(10)) # Show last 10 clean records

    time.sleep(2) # Refresh dashboard every 2 seconds
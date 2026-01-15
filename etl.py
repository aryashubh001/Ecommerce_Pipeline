import sqlite3
import pandas as pd
import json
import time

def run_etl():
    conn = sqlite3.connect('ecommerce.db')
    
    print("🔄 Extracting raw data...")
    # 1. EXTRACT: Read raw logs
    try:
        df_raw = pd.read_sql("SELECT * FROM raw_logs", conn)
    except Exception as e:
        print("No data found. Run producer.py first!")
        return

    if df_raw.empty:
        print("Database is empty. Run producer.py first!")
        return

    # 2. TRANSFORM: Parse JSON column into separate columns
    # This turns the text '{"price": 100...}' into actual columns
    print("🛠️ Transforming and cleaning...")
    json_cols = df_raw['event_data'].apply(json.loads).apply(pd.Series)
    df_clean = pd.concat([df_raw['timestamp'], json_cols], axis=1)

    # DATA CLEANING RULES (Crucial for Microsoft IDEAs)
    initial_count = len(df_clean)
    
    # Rule 1: Drop rows where user_id is missing
    df_clean = df_clean.dropna(subset=['user_id'])
    
    # Rule 2: Drop rows where price is invalid (negative or zero)
    df_clean = df_clean[df_clean['price'] > 0]
    
    removed_count = initial_count - len(df_clean)
    print(f"🧹 Cleaned {removed_count} corrupted records.")

    # 3. LOAD: Save to a new table 'clean_data'
    # 'if_exists=replace' overwrites the table every time we run this script
    df_clean.to_sql('clean_data', conn, if_exists='replace', index=False)
    
    print(f"✅ Success! {len(df_clean)} valid records loaded to 'clean_data'.")
    conn.close()

if __name__ == "__main__":
    while True:
        run_etl()
        print("Sleeping for 10 seconds...")
        time.sleep(10) # Run ETL every 10 seconds to simulate real-time processing
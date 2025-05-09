import pandas as pd
import sqlite3
import os

# --- Configuration ---
csv_file_path = "tournament_stats.csv"  # Replace with your actual CSV path
db_path = "cricket_analysis.db"         # Replace with your actual DB path
table_name = "tournament_stats"

# --- Load CSV ---
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

df = pd.read_csv(csv_file_path)

# --- Connect to SQLite DB ---
conn = sqlite3.connect(db_path)

# --- Save to SQL Table ---
df.to_sql(table_name, conn, if_exists='replace', index=False)

print(f"✅ Table '{table_name}' created/updated successfully in database '{db_path}'.")

# --- Close connection ---
conn.close()

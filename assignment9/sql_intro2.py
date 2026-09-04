import os
import sqlite3
import pandas as pd

# Path to database relative to assignment9 directory
db_path = "./db/lesson.db"

# 1. Connect to SQLite database and query data via JOIN
conn = sqlite3.connect(db_path)

query = """
SELECT 
    line_items.line_item_id,
    line_items.quantity,
    products.product_id,
    products.product_name,
    products.price
FROM line_items
JOIN products ON line_items.product_id = products.product_id;
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Print the first 5 lines of the initial DataFrame
print("--- Step 1: Initial DataFrame (First 5 lines) ---")
print(df.head())
print("\n" + "="*60 + "\n")

# 2. Add 'total' column (quantity * price)
df['total'] = df['quantity'] * df['price']

print("--- Step 2: DataFrame with 'total' Column (First 5 lines) ---")
print(df.head())
print("\n" + "="*60 + "\n")

# 3. Group by product_id and aggregate
# 'line_item_id': 'count' -> times ordered
# 'total': 'sum'          -> total revenue/price paid
# 'product_name': 'first' -> preserve product name
summary_df = df.groupby('product_id', as_index=False).agg({
    'line_item_id': 'count',
    'total': 'sum',
    'product_name': 'first'
})

print("--- Step 3: Aggregated Summary DataFrame (First 5 lines) ---")
print(summary_df.head())
print("\n" + "="*60 + "\n")

# 4. Sort the DataFrame by product_name
summary_df = summary_df.sort_values(by='product_name')

# 5. Export summary DataFrame to order_summary.csv
output_csv = "order_summary.csv"
summary_df.to_csv(output_csv, index=False)

print(f"Successfully generated and saved summary to '{output_csv}'!")
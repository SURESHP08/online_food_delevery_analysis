import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# -------------------------------
# 1. Load Data
# -------------------------------
df = pd.read_csv(r"D:\online food delivery analysisi\ONINE_FOOD_DELIVERY_ANALYSIS.csv")

# Rename columns to consistent snake_case
rename_map = {
    'Customer_Age': 'customer_age',
    'Cuisine_Type': 'cuisine',
    'Delivery_Time_Min': 'delivery_time',
    'Order_Value': 'order_value',
    'Cancellation_Reason': 'cancel_reason',
    'Delivery_Rating': 'rating',
    'Profit_Margin': 'profit_margin',
    'Order_Date': 'order_date',
    'Distance_km': 'distance_km',
    'Order_Status': 'order_status',
    'City': 'city',
    'Peak_Hour': 'peak_hour'
}
df.rename(columns=rename_map, inplace=True)

print(df.head())
print(df.info())
print(df.describe())

# -------------------------------
# 2. Data Cleaning & Preprocessing
# -------------------------------
df.fillna({
    'delivery_time': df['delivery_time'].median(),
    'order_value': df['order_value'].median(),
    'customer_age': df['customer_age'].mode()[0]
}, inplace=True)

df['delivery_time'] = np.where(df['delivery_time'] > df['delivery_time'].quantile(0.95),
                               df['delivery_time'].quantile(0.95),
                               df['delivery_time'])
df['order_value'] = np.where(df['order_value'] > df['order_value'].quantile(0.95),
                             df['order_value'].quantile(0.95),
                             df['order_value'])

df.loc[df['rating'] > 5, 'rating'] = 5
df.loc[df['profit_margin'] < 0, 'profit_margin'] = 0

df['cuisine'] = df['cuisine'].str.strip().str.lower()
df['city'] = df['city'].str.title()
df.loc[df['order_status'] == 'Cancelled', 'rating'] = np.nan

# -------------------------------
# 3. Feature Engineering
# -------------------------------
df['order_date'] = pd.to_datetime(df['order_date'])
df['day_type'] = df['order_date'].dt.dayofweek.apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
df['hour'] = df['order_date'].dt.hour
df['peak_hour'] = df['hour'].apply(lambda x: 1 if (x >= 19 and x <= 22) else 0)
df['profit_margin_pct'] = (df['profit_margin'] / df['order_value']) * 100
df['delivery_perf'] = pd.cut(df['delivery_time'],
                             bins=[0, 30, 60, 120, np.inf],
                             labels=['Fast', 'Moderate', 'Slow', 'Very Slow'])
df['age_group'] = pd.cut(df['customer_age'],
                         bins=[0, 18, 30, 45, 60, np.inf],
                         labels=['Teen', 'Young Adult', 'Adult', 'Middle Age', 'Senior'])

# -------------------------------
# 4. Connect to MySQL
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",       # Change if using remote MySQL
        user="root",            # Your MySQL username
        password="My$QL102511"  # Your MySQL password
    )

    if conn.is_connected():
        print("Connected to MySQL")
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS food_delivery")
        conn.commit()
        cursor.execute("USE food_delivery")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            order_date DATETIME,
            city VARCHAR(100),
            cuisine VARCHAR(100),
            order_value FLOAT,
            delivery_time FLOAT,
            rating FLOAT,
            profit_margin FLOAT,
            day_type VARCHAR(20),
            peak_hour TINYINT,
            profit_margin_pct FLOAT,
            customer_age INT,
            age_group VARCHAR(50),
            delivery_perf VARCHAR(50),
            order_status VARCHAR(50),
            cancel_reason VARCHAR(255),
            distance_km FLOAT
        )
        """)
        conn.commit()

        insert_query = """
        INSERT INTO orders (
            order_date, city, cuisine, order_value, delivery_time, rating,
            profit_margin, day_type, peak_hour, profit_margin_pct,
            customer_age, age_group, delivery_perf, order_status,
            cancel_reason, distance_km
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = []
        for _, row in df.iterrows():
            data.append((
                row['order_date'] if pd.notna(row['order_date']) else None,
                str(row['city']) if pd.notna(row['city']) else None,
                str(row['cuisine']) if pd.notna(row['cuisine']) else None,
                row['order_value'],
                row['delivery_time'],
                row['rating'] if pd.notna(row['rating']) else None,
                row['profit_margin'],
                row['day_type'],
                int(row['peak_hour']) if pd.notna(row['peak_hour']) else None,
                row['profit_margin_pct'],
                int(row['customer_age']) if pd.notna(row['customer_age']) else None,
                str(row['age_group']) if pd.notna(row['age_group']) else None,
                str(row['delivery_perf']) if pd.notna(row['delivery_perf']) else None,
                row['order_status'],
                str(row['cancel_reason']) if pd.notna(row['cancel_reason']) else None,
                row['distance_km'] if pd.notna(row['distance_km']) else None
            ))

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"{cursor.rowcount} rows inserted into MySQL database.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")
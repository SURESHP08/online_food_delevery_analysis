import streamlit as st
import pandas as pd

st.title("📊 Food Delivery Dashboard")

# Load data
df = pd.read_csv(r"D:\online food delivery analysisi\ONINE_FOOD_DELIVERY_ANALYSIS.csv")

# Preview
st.write("Data Preview:", df.head())
st.write("Row count:", len(df))

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(df))
col2.metric("Total Revenue", f"${df['Order_Value'].sum():,.2f}")
col3.metric("Avg Order Value", f"${df['Order_Value'].mean():.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Avg Delivery Time", f"{df['Delivery_Time_Min'].mean():.1f} min")
col5.metric("Cancellation Rate", f"{(df['Order_Status'].eq('Cancelled').mean()*100):.2f}%")
col6.metric("Avg Delivery Rating", f"{df['Delivery_Rating'].mean():.2f}")

st.metric("Profit Margin %", f"{df['Profit_Margin'].mean():.2f}%")

# Monthly revenue trend
st.subheader("Monthly Revenue Trend")
monthly_revenue = df.groupby(pd.to_datetime(df['Order_Date']).dt.to_period('M'))['Order_Value'].sum()
st.line_chart(monthly_revenue)

# Payment mode preferences
st.subheader("Payment Mode Preferences")
if 'Payment_Mode' in df.columns:
    payment_mode_revenue = df.groupby('Payment_Mode')['Order_Value'].sum()
    st.bar_chart(payment_mode_revenue)

# Delivery performance by city
st.subheader("Average Delivery Time by City")
city_delivery = df.groupby('City')['Delivery_Time_Min'].mean()
st.bar_chart(city_delivery)

# Cancellation reasons
st.subheader("Cancellation Reasons")
cancel_reasons = df[df['Order_Status'] == 'Cancelled']['Cancellation_Reason'].value_counts()
st.bar_chart(cancel_reasons)
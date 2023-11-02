import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Create or connect to an SQLite database
conn = sqlite3.connect('ride_data.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ride_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE,
        Customer_Name TEXT,
        Aadhar_Number TEXT,
        DL_No TEXT,
        Phone_Number TEXT,
        Referenced_By TEXT,
        Bike_Number TEXT,
        Ride_Start_Time TEXT, -- Store time as text
        Ride_Start_KM REAL,
        Ride_End_Time TEXT, -- Store time as text
        Ride_Close_KM REAL,
        Total_Duration TEXT,
        Total_KM REAL,
        Advance REAL,
        Plan TEXT,
        Balance REAL,
        Total_Amount REAL,
        Transaction_ID TEXT,
        Feedback TEXT
    )
''')
conn.commit()

# Streamlit app
st.title("Ride Data Collection")

# User input fields
date = st.date_input("Date")
customer_name = st.text_input("Customer Name")
aadhar_number = st.text_input("Aadhar Number")
dl_no = st.text_input("DL No")
phone_number = st.text_input("Phone Number")
referenced_by = st.text_input("Referenced By")
bike_number = st.text_input("Bike Number")
ride_start_time = st.time_input("Ride Start Time")
ride_start_time_str = ride_start_time.strftime("%H:%M:%S")  # Convert to string
ride_start_km = st.number_input("Ride Start KM")
ride_end_time = st.time_input("Ride End Time")
ride_end_time_str = ride_end_time.strftime("%H:%M:%S")  # Convert to string
ride_close_km = st.number_input("Ride Close KM")
total_duration = st.text_input("Total Duration")
total_km = st.number_input("Total KM")
advance = st.number_input("Advance")
plan = st.selectbox("Plan", ["Plan A", "Plan B", "Plan C"])
balance = st.number_input("Balance")
total_amount = st.number_input("Total Amount")
transaction_id = st.text_input("Transaction ID")
feedback = st.text_area("Feedback")

if st.button("Submit"):
    cursor.execute('''
        INSERT INTO ride_data (
            Date, Customer_Name, Aadhar_Number, DL_No, Phone_Number, Referenced_By, 
            Bike_Number, Ride_Start_Time, Ride_Start_KM, Ride_End_Time, Ride_Close_KM, 
            Total_Duration, Total_KM, Advance, Plan, Balance, Total_Amount, Transaction_ID, Feedback
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (
        date, customer_name, aadhar_number, dl_no, phone_number, referenced_by, 
        bike_number, ride_start_time_str, ride_start_km, ride_end_time_str, ride_close_km, 
        total_duration, total_km, advance, plan, balance, total_amount, transaction_id, feedback
    ))
    conn.commit()
    st.success("Data submitted successfully!")

# Display the current data in the database
st.header("Current Ride Data")
data = pd.read_sql('SELECT * FROM ride_data', conn)
st.dataframe(data)

# Close the database connection
conn.close()

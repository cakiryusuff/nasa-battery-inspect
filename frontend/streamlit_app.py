import streamlit as st
import requests

# API endpoint
url = "http://backend:5000/return_prediction" 

st.title("API Data Sender")
with st.form("my_form"):
    voltage_charge = st.number_input("Voltage_charge")
    voltage_measured = st.number_input("Voltage_measured")
    current_measured = st.number_input("current_measured")
    temperature_measured = st.number_input("Temperature_measured")
    time_value = st.number_input("Time")
    
    submitted = st.form_submit_button("Submit")

# Form gönderildiğinde POST isteği
if submitted:
    payload = {
        "Voltage_charge": voltage_charge,
        "Voltage_measured": voltage_measured,
        "Temperature_measured": temperature_measured,
        "Current_measured": current_measured,
        "Time": time_value
    }

    with st.spinner("Veri gönderiliyor..."):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("Veri başarıyla gönderildi!")
                st.json(response.json())
            else:
                st.error(f"Hata: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"İstek hatası: {e}")

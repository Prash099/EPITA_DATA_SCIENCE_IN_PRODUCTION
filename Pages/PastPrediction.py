import streamlit as st
import requests
from fastapi import FastAPI

with st.container():
    st.title("Wine Prediction Model [Past Prediction]")
    st.header("DSP - WineWaalas")
    st.write("- Kirubhaharan Balasubramanian")

with st.container():
    st.write("-----")
    left_column, right_column = st.columns(2)
    with left_column:
        st.date_input("Start Date")
    with right_column:
        st.date_input("End Date")

if st.button('Make prediction'):

    response = requests.get(url="http://127.0.0.1:8000/past_predictions")

    if response.status_code == 200:
        st.subheader(f"Response from API 🚀 = {response.json()}")
    else:
        st.subheader(f"Error from API 😞 = {response.json()}")



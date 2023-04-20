import json
import streamlit as st
from fastapi import FastAPI
import requests
import pandas as pd
import ast

with st.container():
    st.title("Wine Prediction Model [Past Prediction]")
    st.header("DSP - WineWaalas")
    st.write("- Kirubhaharan Balasubramanian")

with st.container():
    st.write("-----")
    left_column, right_column = st.columns(2)
    with left_column:
        s_Date = st.date_input("Start Date")
    with right_column:
        e_Date = st.date_input("End Date")

if st.button('Get Past Predictions'):

    response = requests.get(url="http://127.0.0.1:8000/past_predictions")

    json_string = response.text
    response_dict = json.loads(json_string)
    body = response_dict['prediction_list']['body']
    body = ast.literal_eval(body)

    body = pd.read_json(body)
    selected_columns = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'predicted_quality','created_at']
    df_subset = body.loc[:, selected_columns]

    if response.status_code == 200:
       # st.subheader(f"Response from API 🚀 = {body}")
        st.text((pd.DataFrame(df_subset)))
    else:
        st.subheader(f"Error from API 😞 = {response.json()}")



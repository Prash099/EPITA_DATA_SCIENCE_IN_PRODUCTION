import json
import streamlit as st
from fastapi import FastAPI
import requests
import pandas as pd
import ast


with st.container():
    st.title("Wine Prediction Model [Past Prediction]")
    st.header("DSP - WineWaalas")

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

    # Date Filtering Code 

    final_list = []
    filtered_data = pd.Series()
    for row in body.iterrows():
        f1 = row[1]
        listdata = f1.to_list()
        date_final = listdata[-2].to_pydatetime().date()
        if(date_final >= s_Date and date_final <= e_Date):
            filtered_data = row[1]
            final_list.append(filtered_data)

    # Table Displaying Code

    if response.status_code == 200:
        st.table(pd.DataFrame(final_list))
        final_list.clear()
    else:
        st.subheader(f"Error from API 😞 = {response.json()}")



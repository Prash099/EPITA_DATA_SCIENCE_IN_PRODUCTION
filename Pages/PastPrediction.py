import json
import streamlit as st
import requests
import pandas as pd
import ast
import datetime

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
    
    body = response_dict['prediction_list']
    body = ast.literal_eval(body)
    
    date_list = []
    for item in body:
        created_at = item['created_at']
        created_datetime = datetime.datetime.fromtimestamp(created_at / 1000)  # Assuming the timestamp is in milliseconds
        created_date = created_datetime.date()
        date_list.append(created_date)

    df = pd.DataFrame(body)
    df['created_date_'] = list(date_list)
    filtered_dates = [date for date in date_list if s_Date <= date <= e_Date]
    
    selected_columns = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'predicted_quality','created_date_']
    df_subset = df.loc[:, selected_columns]
    filtered_df = df_subset[df_subset['created_date_'].isin(filtered_dates)]

    if response.status_code == 200:
        st.table((filtered_df))
    else:
        st.subheader(f"Error from API 😞 = {response.json()}")

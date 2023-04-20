import json
import pandas as pd
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from fastapi import FastAPI

app = FastAPI()

st.set_page_config(page_title="My Webpage", page_icon="🍷", layout="wide")


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_RFHPja.json")

with st.container():
    st.title("Wine Prediction Model")
    st.header("DSP - WineWaalas")
    st.write("- Kirubhaharan Balasubramanian")

with st.container():
    st.write("-----")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Description")
        st.write("##")
        st.write("""This datasets is related to red variants of the Portuguese Vinho Verde wine. The dataset 
        describes the amount of various chemicals present in wine and their effect on it's quality. The datasets can 
        be viewed as classification or regression tasks. The classes are ordered and not balanced (e.g. there are 
        much more normal wines than excellent or poor ones).Your task is to predict the quality of wine using the 
        given data. A simple yet challenging project, to anticipate the quality of wine. The complexity arises due to 
        the fact that the dataset has fewer samples, & is highly imbalanced. Can you overcome these obstacles & build 
        a good predictive model to classify them?""")
        st.write("[Learn More >](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset)")

        st.header("Features used to Predict")
        st.write("##")
        st.write("""Input variables (based on physicochemical tests):\n
                    1 - fixed acidity\n
                    2 - volatile acidity\n
                    3 - citric acid\n
                    4 - residual sugar\n
                    5 - chlorides\n
                    6 - free sulfur dioxide\n
                    7 - total sulfur dioxide\n
                    8 - density\n
                    9 - pH\n
                    10 - sulphates\n
                    11 - alcohol""")

    with right_column:
        st_lottie(animation, height=300, key='wine')
        fixed_acidity = st.number_input("Fixed Acidity", format="%.5f")
        volatile_acidity = st.number_input("Volatile Acidity", format="%.5f")
        citric_acid = st.number_input("Citric Acid", format="%.5f")
        residual_sugar = st.number_input("Residual Sugar", format="%.5f")
        chlorides = st.number_input("Chlorides", format="%.5f")
        free_sulfur_dioxide = st.number_input("Free Sulphur Dioxide", format="%.5f")
        total_sulfur_dioxide = st.number_input("Total Sulfur dioxide", format="%.5f")
        density = st.number_input("Density", format="%.5f")
        pH = st.number_input("pH", format="%.5f")
        sulphates = st.number_input("Sulphates", format="%.5f")
        alcohol = st.number_input("Alcohol", format="%.5f")

inputs = {"fixed_acidity": fixed_acidity, "volatile_acidity": volatile_acidity, "citric_acid": citric_acid,
          "residual_sugar": residual_sugar, "chlorides": chlorides, "free_sulfur_dioxide": free_sulfur_dioxide,
          "total_sulfur_dioxide": total_sulfur_dioxide, "density": density, "pH": pH, "sulphates": sulphates,
          "alcohol": alcohol
          }
l1 = list(inputs.values())
l2 = []
l2.append(l1)
print("L2 : ", l2)
if st.button('Predict the Features'):
    res = requests.post(url="http://127.0.0.1:8000/predict", data=json.dumps(l2))

    st.subheader(f"Response from API 🚀 =  {res.text}")

file = st.file_uploader("Insert CSV FILES")

if st.button('Make prediction'):
    csv_file = pd.read_csv(file)
    features_list = csv_file.columns.tolist()
    features_dict = {feature: [] for feature in features_list}

    response = requests.post(url="http://127.0.0.1:8000/make_prediction", data=json.dumps(features_dict))

    if response.status_code == 200:
        st.subheader(f"Response from API 🚀 = {response.json()}")
    else:
        st.subheader(f"Error from API 😞 = {response.json()}")

DATA SCIENCE IN PRODUCTION


## About

This project is used for predicting the quality of wine for the given dataset. We have used the folowing for this project.

- Airflow
- Postgres
- Streamlit
- FastAPI
- Grafana
## Authors

- Prashanth Raghavendra Rao
- Kirubhaharan Balasubramanian
- Arslan
- Yihang




## Installation

To run this project open terminal and run this code.

```bash
  pip install -r requirements.txt
```

After Successful Installing, Do this step to run FastAPI

```bash
  uvicorn main:app
```

To run the WebApp, type the below code

```bash
  streamlit run frontend.py
```

To run the great_expectations, type the below code

```bash
  great_expectations init
```

To run the airflow, type the below code

```bash
  airflow scheduler
```
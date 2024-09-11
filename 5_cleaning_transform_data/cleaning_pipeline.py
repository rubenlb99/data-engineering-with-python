import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2 as db

default_args = {
    'owner': 'ruben',
    'start_date': dt.datetime(2024,9,10),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

def clean_scooter():
    df = pd.read_csv("/home/ruben/nifi-book/5_cleaning_transform_data/scooter.csv")

    df.drop(columns=['region_id'], inplace=True)

    df.columns=[x.lower() for x in df.columns]

    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')

    df.to_csv('/home/ruben/nifi-book/5_cleaning_transform_data/clean_scooter.csv')

def filter_data():
    df = pd.read_csv("/home/ruben/nifi-book/5_cleaning_transform_data/clean_scooter.csv")

    from_day = '2019-05-23'
    to_day = '2019-06-03'

    tofrom = df[(df['started_at']>from_day) & (df['started_at']<to_day)]

    tofrom.to_csv('/home/ruben/nifi-book/5_cleaning_transform_data/may23-june23.csv')

with DAG('CleanScooterDAG', default_args=default_args, schedule=timedelta(minutes=5)) as dag:
    cleanScooter = PythonOperator(task_id='cleanScooter', python_callable=clean_scooter)
    filterData = PythonOperator(task_id='filterData', python_callable=filter_data)


cleanScooter >> filterData
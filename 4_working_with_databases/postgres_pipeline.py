import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2 as db

default_args = {
    'owner': 'ruben',
    'start_date': dt.datetime(2024,9,8),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

def get_data_from_postgres():
    conn_string = "dbname='nifi_db' host='localhost' user='root' password='root'"

    conn=db.connect(conn_string)

    df = pd.read_sql("select name, city from users", conn)

    df.to_csv("/home/ruben/nifi-book/4_working_with_databases/postgresqldata.csv")

def transform_to_json():
    df = pd.read_csv("/home/ruben/nifi-book/4_working_with_databases/postgresqldata.csv")

    df.to_json("/home/ruben/nifi-book/4_working_with_databases/postgresqldata.json", orient='records', lines=True)

with DAG('PostgresExtractDAG', default_args=default_args, schedule=timedelta(minutes=5)) as dag:
    getData = PythonOperator(task_id='convertCSVtoJson', python_callable=get_data_from_postgres)
    transformCSVtoJSON = PythonOperator(task_id='transformCSVtoJSON', python_callable=transform_to_json)

getData >> transformCSVtoJSON



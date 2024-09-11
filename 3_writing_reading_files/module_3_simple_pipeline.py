import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd

def CSVtoJSON():
    df=pd.read_csv('/home/ruben/nifi-book/3_writing_reading_files/data.csv')
    for i,r in df.iterrows():
        print(r['name'])
    df.to_json('/home/ruben/nifi-book/3_writing_reading_files/fromAirflow.json', orient='records')

default_args = {
    'owner': 'ruben',
    'start_date': dt.datetime(2024,9,6),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

with DAG('MyCSVDAG', default_args=default_args, schedule=timedelta(minutes=5)) as dag:
    print_starting = BashOperator(task_id='starting', bash_command='echo "I am reading the csv..."')
    CSVJson = PythonOperator(task_id='convertCSVtoJson', python_callable=CSVtoJSON)

print_starting >> CSVJson

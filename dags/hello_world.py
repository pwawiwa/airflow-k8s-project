from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def hello_world():
    print("Hello World from Airflow on Kubernetes!")

with DAG(
    dag_id="hello_world_k8s",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:
    task1 = PythonOperator(
        task_id="say_hello",
        python_callable=hello_world
    )

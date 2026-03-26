from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def process_data(**kwargs):
    print("Processing some complex data...")
    return "Data Processed"

with DAG(
    'complex_k8s_workflow',
    default_args=default_args,
    description='A complex DAG for K8s playground',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['playground', 'k8s'],
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = PythonOperator(
        task_id='process_data_task',
        python_callable=process_data,
        provide_context=True,
    )

    t3 = BashOperator(
        task_id='sleep_task',
        depends_on_past=False,
        bash_command='sleep 5',
        retries=3,
    )

    t4 = BashOperator(
        task_id='templated_task',
        depends_on_past=False,
        bash_command="""
            {% for i in range(5) %}
                echo "{{ ds }}"
                echo "{{ params.my_param }}"
            {% endfor %}
        """,
        params={'my_param': 'Parameter Value'},
    )

    t1 >> [t2, t3] >> t4

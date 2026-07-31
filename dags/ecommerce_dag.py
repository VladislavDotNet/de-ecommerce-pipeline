from datetime import datetime, timedelta
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'de_user',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_etl_script():
    # Запуск нашего скрипта прямо внутри контейнера Airflow
    result = subprocess.run(["python", "/opt/airflow/etl_pipeline.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"ETL failed: {result.stderr}")
    print(result.stdout)

with DAG(
    'ecommerce_etl_pipeline',
    default_args=default_args,
    description='Ежедневный запуск ETL для магазина',
    schedule_interval='0 2 * * *',  # Каждый день в 02:00
    catchup=False,
) as dag:

    run_etl_task = PythonOperator(
        task_id='run_etl_pipeline',
        python_callable=run_etl_script,
    )
from resources.rsrc_ocorrencia import batch_run, check_for_update, write_on_db
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'victor',
    'retries': 5,
    'retry_delay': timedelta(days=1)
}



with DAG(
    default_args=default_args,
    dag_id="dag_ocorrencia",
    catchup=False,
    start_date = datetime(2022, 11, 1),
    schedule_interval='@daily'
) as dag:
    check_updates = BranchPythonOperator(
        task_id = 'check_for_update',
        python_callable = check_for_update
    )
    up_to_date = DummyOperator(
        task_id = 'up_to_date'
    )
    writes_db = PythonOperator(
        task_id = 'write_on_db',
        python_callable = write_on_db
    )

    done = DummyOperator(
        task_id = 'Done',
        trigger_rule='none_failed_or_skipped'
    )


check_updates >> [up_to_date, writes_db] >> done
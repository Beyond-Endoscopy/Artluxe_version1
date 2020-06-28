from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

bashcommand1 = "python3 ~/Artluxe_version1/new_auctions_collector.py"

bashcommand2 = "python3 ~/Artluxe_version1/upcoming_online.py"

with DAG(dag_id = 'upcoming_work', scheduler_interval = @weekly,
     start_date = datetime(2020, 1, 1), catchup=False) as dag:

    dummy_task = DummyOperator(task_id='dummy_task')

    collect_auctions = BashOperator(task_id='collect_auctions', bash_command=bashcommand1)

    artworks = BashOperator(task_id='artworks', bash_command=bashcommand2)

    dummy_task >> collect_auctions >> artworks



from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

bashcommand1 = "python3 ~/Artluxe_version1/upcoming_scraper/new_auctions_collector.py"

bashcommand2 = "python3 ~/Artluxe_version1/upcoming_scraper/upcoming_scraper_job.py"

bashcommand3 = "python3 ~/Artluxe_version1/upcoming_scraper/to_database.py"

bashcommand4 = "python3 ~/Artluxe_version1/upcoming_scraper/monitor_to_db.py"


with DAG(dag_id = 'upcoming_work', scheduler_interval = @weekly,
     start_date = datetime(2020, 1, 1), catchup=False) as dag:

    dummy_task = DummyOperator(task_id='dummy_task')

    collect_auctions = BashOperator(task_id='collect_auctions', bash_command=bashcommand1)

    artworks = BashOperator(task_id='artworks', bash_command=bashcommand2)

    insert_data = BashOperator(task_id='insert_data', bash_command=bashcommand3)

    running_info = BashOperator(task_id='running_info', bash_command=bashcommand4)

    dummy_task >> collect_auctions >> artworks
    artworks >> insert_data
    artworks >> running_info



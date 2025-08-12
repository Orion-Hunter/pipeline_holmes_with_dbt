from datetime import datetime, date, timedelta
from airflow import DAG
from app.domain.value_objects import PipelineExecutionType
from tasks.process_pipeline_execution import execute_process_etl

default_args = {
    'owner': 'airflow',
    'retries': 1,
}
with DAG(
        dag_id = 'process_etl_full_dag',
        description = 'Dag to ETL Process Pipeline',
        default_args = default_args,
        start_date=datetime(2024, 6, 1),
        schedule_interval = None, 
        catchup = False, 
        tags = ['process', 'etl'],
) as dag:
    
    execute_process_etl(
        start_date=date(2024,6,1).strftime("%d/%m/%Y"),
        end_date=(date.today() - timedelta(days=1)).strftime("%d/%m/%Y"),  
        rule=PipelineExecutionType.FULL
    )


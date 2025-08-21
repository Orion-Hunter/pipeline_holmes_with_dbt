from datetime import datetime, timedelta
from airflow import DAG
from app.domain.value_objects import PipelineExecutionType
from tasks.process_pipeline_execution import execute_process_etl

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
with DAG(
        dag_id = 'etl_holmes_canceling_refresh_process',
        description = 'Dag to ETL Process Pipeline',
        default_args = default_args,
        start_date=datetime(2024, 6, 1),
        schedule_interval = '0 16 * * 6', 
        catchup = False, 
        tags = ['process', 'etl'],
) as dag:
    
    execute_process_etl(
        start_date=datetime.now().date().strftime("%d/%m/%Y"),
        end_date=datetime.now().date().strftime("%d/%m/%Y"),  
        rule=PipelineExecutionType.REFRESH
    )


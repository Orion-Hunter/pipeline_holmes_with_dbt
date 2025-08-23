from datetime import datetime, date, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator 
from app.domain.value_objects import PipelineExecutionType
from tasks.process_extraction import process_extraction
from tasks.process_transformation import process_transformation
from tasks.process_load import process_load

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

@task.branch
def check_extraction(data):
    if isinstance(data, list) and len(data) > 0:
        return "transform"   
    return "end"      


with DAG(
        dag_id = 'process_etl_full_dag',
        description = 'Dag to ETL Process Pipeline',
        default_args = default_args,
        start_date=datetime(2024, 6, 1),
        schedule_interval = None, 
        catchup = False, 
        tags = ['process', 'etl'],
) as dag:
    
    raw_data_process = process_extraction.override(task_id="extract")(
        start_date=date(2024,6,1).strftime("%d/%m/%Y"),
        end_date=(date.today() - timedelta(days=1)).strftime("%d/%m/%Y"),
        rule=PipelineExecutionType.FULL
    )  
    check = check_extraction(raw_data_process)
    transformed_data_process = process_transformation.override(task_id='transform')(raw_data_process)
    load = process_load.override(task_id='load')(data=transformed_data_process, rule=PipelineExecutionType.FULL)

    end = EmptyOperator(task_id="end")
 
    raw_data_process >> check
    check >> transformed_data_process >> load
    check >> end




   
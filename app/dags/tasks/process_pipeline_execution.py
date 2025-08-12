import asyncio
from airflow.decorators import task
from dotenv import load_dotenv, dotenv_values
from datetime import date
from app.domain.value_objects import PipelineExecutionType   
from app.config.log_config import logger  
@task
def execute_process_etl(start_date: date, end_date: date, rule: PipelineExecutionType):
    
    try: 
        load_dotenv()
        raw_env = dotenv_values('.env')
        database_url=raw_env['DATABASE_URL']
        if database_url is None:
            raise Exception("Datawarehouse credential not found!")
 
   
        from app.data.database import AsyncDatabase
        from app.infra.etl.canceling_process_etl_service import CancelingProcessServiceETL
        database = AsyncDatabase(database_url)
    
        async def run_etl():
            service = CancelingProcessServiceETL(
                database,
                start_date,
                end_date,
                rule
            )

            res = await service.execute()
            return res
    
        result = asyncio.run(run_etl())
        logger.info(f"ETL RESULT: {result}")
       
    except Exception as e:
        logger.error(f"ETL ERROR: {e}")
        raise


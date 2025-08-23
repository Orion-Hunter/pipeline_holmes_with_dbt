import asyncio
from typing import Any, List
from airflow.decorators import task
from dotenv import load_dotenv, dotenv_values 
from app.config.log_config import logger  

@task
def process_transformation(data: List[Any]):
    
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
            service = CancelingProcessServiceETL(database)

            res = await service.transform(data)
            return res
    
        result = asyncio.run(run_etl())
        logger.info(f"TRANSFORMATION RESULT: {result}")
        return result
    except Exception as e:
        logger.error(f"TRANSFORMATION ERROR: {e}")
        raise


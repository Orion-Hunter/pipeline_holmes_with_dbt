import os, asyncio 
from dotenv import load_dotenv 
from domain.value_objects import PipelineExecutionType
from infra.etl.canceling_process_etl_service import CancelingProcessServiceETL
from data.database import AsyncDatabase
from datetime import date
from config.log_config import logger


load_dotenv()
database = AsyncDatabase(os.getenv('DATABASE_URL'))
service = CancelingProcessServiceETL(database,
                                    start_date=date(2024,6,1).strftime("%d/%m/%Y"),
                                    end_date=date(2025,8,5).strftime("%d/%m/%Y"),
                                    rule=PipelineExecutionType.APPEND 
                                    )

async def main():
    
   result = await asyncio.gather(*[service.execute()], return_exceptions=True) 
   
   if result[0].is_err():
      logger.error(f"Pipeline {service.__class__.__name__}  execution ended! Result is fail: {result[0].unwrap_err()}")

   logger.info(f"Pipeline {service.__class__.__name__}  execution ended! Result: {result[0].unwrap()}")
    
   
if __name__ == '__main__':
   asyncio.run(main())
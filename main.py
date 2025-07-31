import os, asyncio 
from dotenv import load_dotenv
from app.domain.value_objects import PipelineExecutionType
from app.infra.etl.canceling_process_etl_service import CancelingProcessServiceETL
from app.data.database import AsyncDatabase
from datetime import date

load_dotenv()
database = AsyncDatabase(os.getenv('DATABASE_URL'))
service = CancelingProcessServiceETL(database,
                                    start_date=date(2024,6,1).strftime("%d/%m/%Y"),
                                    end_date=date(2025,7,23).strftime("%d/%m/%Y"),
                                    rule=PipelineExecutionType.FULL 
                                    )

async def main():
   res = await service.execute()
   print(res)


if __name__ == '__main__':
   asyncio.run(main())


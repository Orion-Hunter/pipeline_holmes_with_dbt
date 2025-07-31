from datetime import date
from typing import List
from data.database import AsyncDatabase
from data.models.silver import Processos
from domain.repositories.repository import Repository
from sqlalchemy import delete, and_

class SQLALchemyProcessRepository(Repository):
    
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def create(self, data: List[Processos]) -> None:
        async with self._database.session_factory() as session:
                session.add_all(data)
                await session.flush()
                await session.commit()

    async def get(self, id: str) -> object:
        ...
    
    async def delete(self) -> None:
        async with self._database.session_factory() as session:
            stmt = delete(Processos)
            await session.execute(stmt)
            await session.commit()
    
    
    async def delete_by_interval(self, start_date: date, end_date: date) -> None:
        async with self._database.session_factory() as session:
            stmt = delete(Processos).where(and_(Processos.data_de_criacao >= start_date,
                           Processos.data_de_criacao <= end_date))
            await session.execute(stmt)
            await session.commit()

    async def get_all(self) -> List[object]:
        ...

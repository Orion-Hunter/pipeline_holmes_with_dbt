from datetime import date
from typing import List
from app.data.database import AsyncDatabase
from app.data.models.silver import Processos
from app.domain.repositories.repository import Repository
from sqlalchemy import delete, and_, select, update

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

    async def update(self, processo: Processos) -> None:  
         async with self._database.session_factory() as session:   
            statement = (
            update(Processos)
            .where(
                and_(
                    Processos.id==processo.id
                )
            )
            .values(
                    data_conclusao=processo.data_conclusao,
                    status=processo.status,
                    ultima_alteracao=processo.ultima_alteracao
            )
            )

            await session.execute(statement=statement)
            await session.flush()
            await session.commit()


    async def get_open_process(self) -> List[Processos]:
         async with self._database.session_factory() as session:
            stmt = ( 
            select(
                    Processos.id,
                    Processos.titulo,
                    Processos.autor,
                    Processos.data_de_criacao,
                    Processos.data_conclusao,
                    Processos.status,
                    Processos.empresa_pela_qual_a_nota_foi_emitida,
                    Processos.empresa_solicitante_do_cancelamento,
                    Processos.categoria_do_cancelamento,
                    Processos.justificativa_da_solicitacao_de_cancelamento,
                    Processos.tipo_da_nota,
                    Processos.numero_da_nota,
                    Processos.nota_possui_boleto,
                    Processos.ultima_alteracao
            )
            .where(
                Processos.data_conclusao.is_(None)
            )
            )
            result = await session.execute(stmt)
            rows = result.fetchall()
            if not rows:
              return None
            return [
                Processos(
                    id = row.id,
                    titulo = row.titulo,
                    autor=row.autor,
                    data_de_criacao=row.data_de_criacao,
                    data_conclusao=row.data_conclusao,
                    status=row.status,
                    empresa_pela_qual_a_nota_foi_emitida=row.empresa_pela_qual_a_nota_foi_emitida,
                    empresa_solicitante_do_cancelamento=row.empresa_solicitante_do_cancelamento,
                    categoria_do_cancelamento=row.categoria_do_cancelamento,
                    justificativa_da_solicitacao_de_cancelamento=row.justificativa_da_solicitacao_de_cancelamento,
                    tipo_da_nota=row.tipo_da_nota,
                    numero_da_nota=row.numero_da_nota,
                    nota_possui_boleto=row.nota_possui_boleto,
                    ultima_alteracao=row.ultima_alteracao
                )
                for row in rows
            ]

    

from sqlalchemy import Column, DateTime, String, Boolean

from data.base import Base

class Processos(Base):
    __tablename__ = "processos"
    __table_args__ = {'schema': 'silver'}
    
    id = Column(String, primary_key = True)
    titulo = Column(String)
    autor=Column(String)
    data_de_criacao=Column(DateTime(timezone=True))
    data_conclusao=Column(DateTime(timezone=True), nullable = True)
    status=Column(String)
    empresa_pela_qual_a_nota_foi_emitida=Column(String)
    empresa_solicitante_do_cancelamento=Column(String)
    categoria_do_cancelamento=Column(String, nullable = True)
    justificativa_da_solicitacao_de_cancelamento=Column(String)
    tipo_da_nota=Column(String)
    numero_da_nota=Column(String)
    nota_possui_boleto=Column(Boolean, nullable = True)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    


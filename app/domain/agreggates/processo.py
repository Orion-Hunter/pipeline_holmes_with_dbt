from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Processo:   
   id: str 
   titulo: str 
   autor: str 
   data_de_criacao: datetime 
   data_conclusao: Optional[datetime] 
   status: str 
   empresa_pela_qual_a_nota_foi_emitida: str
   empresa_solicitante_do_cancelamento: str 
   categoria_do_cancelamento: Optional[str]
   justificativa_da_solicitacao_de_cancelamento: str 
   tipo_da_nota: str 
   numero_da_nota: str 
   nota_possui_boleto: str
   
   
   def get_dict(cls):
     return asdict(cls)

   @classmethod
   def create(cls, 
                id: str, 
                titulo: str, 
                autor: str, 
                data_de_criacao: datetime, 
                data_conclusao: Optional[datetime], 
                status: str, 
                empresa_pela_qual_a_nota_foi_emitida: str,
                empresa_solicitante_do_cancelamento: str, 
                categoria_do_cancelamento: Optional[str],
                justificativa_da_solicitacao_de_cancelamento: str, 
                tipo_da_nota: str, 
                numero_da_nota: str, 
                nota_possui_boleto: str
              ) -> "Processo":
                
                processo = Processo(
                   id=id, 
                   titulo=titulo,
                   autor=autor, 
                   data_de_criacao=data_de_criacao, 
                   data_conclusao=data_conclusao, 
                   status=status, 
                   empresa_pela_qual_a_nota_foi_emitida=empresa_pela_qual_a_nota_foi_emitida,
                   empresa_solicitante_do_cancelamento=empresa_solicitante_do_cancelamento, 
                   categoria_do_cancelamento=categoria_do_cancelamento,
                   justificativa_da_solicitacao_de_cancelamento=justificativa_da_solicitacao_de_cancelamento, 
                   tipo_da_nota=tipo_da_nota, 
                   numero_da_nota=numero_da_nota, 
                  nota_possui_boleto=nota_possui_boleto     
                )

                return processo
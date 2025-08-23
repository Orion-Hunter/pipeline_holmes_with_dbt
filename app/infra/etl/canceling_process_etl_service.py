import json
import os
import time
import pandas as pd
from datetime import datetime
from result import Ok, Err

from app.data.database import AsyncDatabase
from app.data.models.silver import Processos
from app.domain.agreggates.processo import Processo
from app.domain.errors import LoadError, TransformError, ExtractError
from app.domain.etl_service import ETLService
from httpx import Timeout
from typing import List, Union, Any
from app.domain.value_objects import PipelineExecutionType, PipelinePayload, DataLayer, BodyGroupTermFilter
from dataclasses import asdict
from app.infra.repositories.SQLALchemy_process_repository import SQLALchemyProcessRepository
from app.infra.services.http_resources_service import HttpResourcesService
from app.infra.etl.rules.values_to_replace import OLD_KEYS_ACCESS
from app.infra.etl.utils.data_treatments import clean_string, safe_to_utc, convert_nat_to_pydatetime
from app.config.log_config import logger

class CancelingProcessServiceETL(ETLService):
    def __init__(self, database: AsyncDatabase):
        self._database = database
        self._repository = SQLALchemyProcessRepository(self._database)   
        
       
    

    
    
    async def __transform_record(self, raw_process) -> Processo:


        properties = {}
       
        user_cache = {}
        identifiers_to_exclude = ["empresa_pela_qual_a_nota_foi_emitida", "empresa_solicitante_do_cancelamento", 
                                  "tipo_da_nota"]  
           
        for prop in raw_process.get('props', []):
            identifier = prop.get('identifier')
            key = prop.get('key')
            value = prop.get('value')

            if identifier:
                if identifier in identifiers_to_exclude:
                     properties[prop['identifier']] =  prop['value']
                else:
                    properties[identifier] = prop.get('label', value)
            elif  key in OLD_KEYS_ACCESS:
                    properties[OLD_KEYS_ACCESS[key]] = value  
          
        
            properties.pop('informativo', None)

        

        possui_boleto = clean_string(properties.get('nota_possui_boleto', '')) == 'Sim'
      
        autor_id = raw_process['author_id']
        if autor_id not in user_cache:
            user_cache[autor_id] = await HttpResourcesService.get_user(autor_id)
        autor = user_cache[autor_id]   

        processo = Processo.create(       
                    id=raw_process['process_id'],
                    titulo=clean_string(raw_process['identifier']),
                    autor=autor,
                    data_de_criacao = safe_to_utc(raw_process['created_at']),
                    data_conclusao = safe_to_utc(raw_process['completed_at']) if raw_process['completed_at'] != None else None,
                    status=raw_process['status'],
                    empresa_pela_qual_a_nota_foi_emitida=clean_string(properties['empresa_pela_qual_a_nota_foi_emitida']) if 'empresa_pela_qual_a_nota_foi_emitida' in properties else ' ',
                    empresa_solicitante_do_cancelamento=clean_string(properties['empresa_solicitante_do_cancelamento']) if 'empresa_solicitante_do_cancelamento' in properties else ' ',
                    categoria_do_cancelamento=clean_string(properties['categoria_do_cancelamento']) if 'categoria_do_cancelamento' in properties else None,
                    justificativa_da_solicitacao_de_cancelamento=clean_string(properties['justificativa_da_solicitacao_de_cancelamento']) if 'justificativa_da_solicitacao_de_cancelamento' in properties else ' ',
                    tipo_da_nota=clean_string(properties['tipo_da_nota']) if 'tipo_da_nota' in properties else ' ',
                    numero_da_nota=clean_string(properties['numero_da_nota']) if 'numero_da_nota' in properties else ' ',
                    nota_possui_boleto=possui_boleto,
                    ultima_alteracao=safe_to_utc(raw_process['updated_at'])
                    )
        return processo
    
    

       
    async def extract(self, execution_rule: PipelineExecutionType, start_date: str, end_date: str) -> Union[List[Any], None]:
        try:
            groups = [
                    {
                        "match_all":True,
                        "terms": [
                            asdict(BodyGroupTermFilter(name="Fluxos", value="64543ee0255042008f58a4a0",
                                              type="is",filter="HProcessFilter",
                                              field="template_id",nested=False)),

                            asdict(BodyGroupTermFilter(name="Situação", value="canceled",
                                              type="isnot",filter="HProcessStatusFilter",
                                              field="status",nested=False)),

                            asdict(BodyGroupTermFilter(name="Data de criação", value=json.dumps({"from":start_date,
                                                        "to":end_date}),
                                              type="period",filter="HDateRange",
                                              field="created_at",nested=False))],
                            "not_used":False
                    }]

            if execution_rule is PipelineExecutionType.REFRESH:
                res = await self._repository.get_open_process()    
                groups = []
            if res:
                for r in res:
                    group = {
                        "match_all":True,
                        "terms": [
                            asdict(BodyGroupTermFilter(name="Fluxos", value="64543ee0255042008f58a4a0",
                                          type="is",filter="HProcessFilter",
                                          field="template_id",nested=False)),
                            asdict(BodyGroupTermFilter(name="ID do processo", value=str(r.id),
                                          type="is",filter="HMatchFilter",
                                          field="_id",nested=False))              
                        ],
                        "not_used":False
                }

                    groups.append(group)

        
            body = {
            "query":{
                "from":0,
                "size":1000,
                "context":"process",
                "groups": groups
        }, "trash":False, "deleted_by_me":False}
         

            extraction_res = await HttpResourcesService.fetch_paginated_results("https://app-api.holmesdoc.io/v2/search",
                                                              headers = {"api_token":os.getenv('HOLMES_TOKEN'),
                                                                         "Content-Type":"application/json"},
                                                              initial_body = body,
                                                              timeout = Timeout(connect = 5.0,read = 60.0,
                                                                                write = 60.0, pool = 5.0),
                                                              step = 200)    
            if len(extraction_res) > 0:
                return extraction_res   
            elif len(extraction_res) == 0:
                logger.info("No data extracted! There is no items to extract!")
                return []
       
            return None
        except Exception as e:
            raise ExtractError(e)
        
        
    async def load(self, data: pd.DataFrame, execution_rule: PipelineExecutionType) -> None:   
        if data is None or len(data) == 0:
           return None
        


        try:
            processos = [
                Processos(**{k: convert_nat_to_pydatetime(v) for k, v in row.items()})
                for row in data.to_dict(orient="records")]

                


            if execution_rule == PipelineExecutionType.REFRESH:
                for processo in processos:
                    await self._repository.update(processo)
            
            elif execution_rule == PipelineExecutionType.APPEND:
                await self._repository.create(processos)   

            elif execution_rule == PipelineExecutionType.FULL: 
                await self._repository.delete()
                await self._repository.create(processos)
            logger.info(f'{len(processos)} loaded in datawarehouse!')
            return None
        except Exception as e:
            raise LoadError(e)
   
        
    async def transform(self, data: List[Any]) -> Union[pd.DataFrame, None]:
        try:
            if data is None or len(data) == 0:
                return None


            items = []
       
            for raw in data:
                item_transformed = await self.__transform_record(raw) 
                items.append(item_transformed)
             
        

            dataframe = pd.DataFrame(items)
            dataframe['data_de_criacao'] = dataframe['data_de_criacao'].dt.tz_localize(None)
            dataframe['data_conclusao'] = pd.to_datetime(dataframe['data_conclusao'], errors='coerce')
            dataframe['data_conclusao'] = dataframe['data_conclusao'].dt.tz_localize(None)
            return dataframe   
        
        except Exception as e:
           raise TransformError(e)
        
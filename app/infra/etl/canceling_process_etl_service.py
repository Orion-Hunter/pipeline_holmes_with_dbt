import json
import os
import time
import pandas as pd
from datetime import datetime
import logging
from result import Ok, Err

from data.database import AsyncDatabase
from data.models.silver import Processos
from domain.agreggates.processo import Processo
from domain.errors import LoadError, TransformError, ExtractError
from domain.etl_service import ETLService
from httpx import Timeout
from typing import List, Union, Any
from domain.value_objects import PipelineExecutionType, PipelinePayload, DataLayer
from dataclasses import asdict
from infra.repositories.SQLALchemy_process_repository import SQLALchemyProcessRepository
from infra.services.http_resources_service import HttpResourcesService
from infra.etl.rules.values_to_replace import OLD_KEYS_ACCESS
from infra.etl.utils.data_treatments import clean_string, safe_to_utc
from config.log_config import logger

class CancelingProcessServiceETL(ETLService):
    def __init__(self, database: AsyncDatabase, start_date: str, end_date: str, rule: PipelineExecutionType):
        self._database = database
        
       
        self.start_date = start_date
        self.end_date = end_date
        self.rule = rule.value
        
        self._payload = json.dumps(asdict(PipelinePayload(
            etl = self.__class__.__name__,
            start_date = start_date,
            end_date = end_date,
            data_layer = DataLayer.SILVER.value
        )), default = HttpResourcesService.json_default)
    
    

    
    
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
                    data_de_criacao = safe_to_utc(datetime.fromisoformat(raw_process['created_at'].replace('Z', '+00:00'))),
                    data_conclusao = safe_to_utc(datetime.fromisoformat(raw_process['completed_at'].replace('Z', '+00:00'))) if raw_process['completed_at'] != None else None,
                    status=raw_process['status'],
                    empresa_pela_qual_a_nota_foi_emitida=clean_string(properties['empresa_pela_qual_a_nota_foi_emitida']) if 'empresa_pela_qual_a_nota_foi_emitida' in properties else ' ',
                    empresa_solicitante_do_cancelamento=clean_string(properties['empresa_solicitante_do_cancelamento']) if 'empresa_solicitante_do_cancelamento' in properties else ' ',
                    categoria_do_cancelamento=clean_string(properties['categoria_do_cancelamento']) if 'categoria_do_cancelamento' in properties else None,
                    justificativa_da_solicitacao_de_cancelamento=clean_string(properties['justificativa_da_solicitacao_de_cancelamento']) if 'justificativa_da_solicitacao_de_cancelamento' in properties else ' ',
                    tipo_da_nota=clean_string(properties['tipo_da_nota']) if 'tipo_da_nota' in properties else ' ',
                    numero_da_nota=clean_string(properties['numero_da_nota']) if 'numero_da_nota' in properties else ' ',
                    nota_possui_boleto=possui_boleto)
        return processo
    
    async def execute(self) -> Union[Ok, Err]:
        
        start_time = time.time()
        logger.info(f"[{datetime.now().isoformat()}] Starting pipeline: {self.__class__.__name__}")
        data = await self.extract()
        if data is None or not isinstance(data, List):
             return ExtractError(data)
        
        if len(data) == 0:
             return Ok("No data extracted! There is no items to extract!")

        data = await self.transform(data)
        if not isinstance(data, pd.DataFrame):
            return TransformError(data)
        
        res = await self.load(data)
        if res != None:
            return LoadError(res)
        
        end_time = time.time()
        return Ok(f'Pipeline {self.__class__.__name__} succesfull executed - Duration {end_time-start_time:.2f} seconds!')
      

       
    async def extract(self) -> Union[List[Any], None]:
        
        
        body = {
            "query":{
                "from":0,
                "size":1000,
                "context":"process",
                "groups":[
                    {
                        "match_all":True,
                        "terms":[
                            {
                                "name":"Fluxos",
                                "value":"64543ee0255042008f58a4a0",
                                "type":"is",
                                "filter":"HProcessFilter",
                                "field":"template_id",
                                "label":"499.2 Solicitação Cancelamento de Notas Fiscais"
                            },
                            {
                                "field":"status",
                                "label":"Cancelado",
                                "name":"Situação",
                                "type":"isnot",
                                "value":"canceled",
                                "filter":"HProcessStatusFilter",
                                "nested":False
                            },
                            {
                                "field":"created_at",
                                "filter":"HDateRange",
                                "name":"Data de criação",
                                "type":"period",
                                "value":json.dumps({"from":self.start_date,
                                                    "to":self.end_date}),
                                "label":None,
                                "nested":False,
                                "id":"bdb99880-1fa4-11f0-9a7c-37cd95193115"
                            }
                        ],
                        "properties":[
                            None,
                            {
                                "name":"Autor",
                                "filter":"HAuthorFilter",
                                "field":"author_id",
                                "type":"is"
                            },
                            {
                                "name":"Data de criação",
                                "filter":"HDateRange",
                                "field":"created_at",
                                "type":"today"
                            },
                            {
                                "name":"Concluído em",
                                "filter":"HDateRange",
                                "field":"completed_at",
                                "type":"today"
                            },
                            {
                                "name":"Situação",
                                "filter":"HProcessStatusFilter",
                                "field":"status",
                                "type":"is"
                            },
                            {
                                "name":"Título",
                                "filter":"HStringFilter",
                                "field":"identifier",
                                "type":"is"
                            },
                            {
                                "name":"Protocolo",
                                "filter":"HStringFilter",
                                "field":"protocol",
                                "type":"is"
                            },
                            {
                                "name":"Status do processo",
                                "filter":"HProcessTestFilter",
                                "field":"test",
                                "type":"is"
                            },
                            {
                                "name":"ID do processo",
                                "filter":"HMatchFilter",
                                "field":"_id",
                                "type":"is"
                            }
                        ],
                        "not_used":False
                    }
                ]
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
            return []
       
        return None
        
        
    async def load(self, data: pd.DataFrame) -> None:
        repository = SQLALchemyProcessRepository(self._database)   
        
        processos = []
        for _, row in data.iterrows(): 
            processos.append(Processos(**row.to_dict()))
            

        if self.rule == PipelineExecutionType.BACKFILL.value:
            await repository.delete_by_interval(self.start_date, self.end_date)   

        elif self.rule == PipelineExecutionType.FULL.value: 
            await repository.delete()

        await repository.create(processos)

        return None
   
        
    async def transform(self, data: List[Any]) -> pd.DataFrame:
          
        items = []
       
        for raw in data:
            try:
                item_transformed = await self.__transform_record(raw) 
                items.append(item_transformed)
            except Exception as e:
                print(e, raw)   
        

        dataframe = pd.DataFrame(items)
     
        dataframe['data_conclusao'] = dataframe['data_conclusao'].replace({pd.NaT: None})

        return dataframe   
        
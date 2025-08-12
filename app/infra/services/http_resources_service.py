from dataclasses import asdict
from datetime import date, datetime
from enum import Enum
import json
import os
from httpx import AsyncClient, Timeout

from app.domain.value_objects import ResponsePayload


class HttpResourcesService:

    @staticmethod 
    async def fetch_paginated_results(base_url, headers, initial_body, timeout: Timeout, step = 200):
        all_results = []
        from_offset = 0
        
        async with AsyncClient() as client:
            while True:
                body = initial_body.copy()
                body["query"]["from"] = from_offset
                body["query"]["size"] = step
                
                response = await client.post(base_url, json = body, headers = headers, timeout = timeout)
                response.raise_for_status()
                data = json.loads(response.content.decode('utf-8'))
                docs = data['docs']
                if not docs:
                    break
                all_results.extend(docs)
                
                if len(docs) < step:
                    break
                from_offset += step
        
        return all_results
    
      
    @staticmethod
    def build_response(method: str, message: str) -> str:
        return json.dumps(asdict(ResponsePayload(
            method = method,
            message = message
        )), default = HttpResourcesService.json_default)
    
    
    @staticmethod
    async def get_user(id: str):
        async with AsyncClient() as client:
            res = await client.get(
                f"https://app-api.holmesdoc.io/v1/admin/users/{id}",
                headers = {"api_token":os.getenv('HOLMES_TOKEN'), "Content-Type":"application/json"},
                timeout = Timeout(connect = 10.0,read = 10.0,write = 10.0,pool = 5.0)
            )
           
            data = json.loads(res.content.decode('utf-8'))
            return data['user']['name']
     

    @staticmethod 
    def json_default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        raise TypeError(f"Type {type(obj)} not serializable")
    
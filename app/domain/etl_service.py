from abc import ABC, abstractmethod
from typing import Dict, List, Any


class ETLService(ABC):
    


    
    @abstractmethod
    async def execute(self):
        ...
    
    @abstractmethod
    async def extract(self):
        ...
    
    @abstractmethod
    async def load(self, data: List[Any]):
        ...
    
    @abstractmethod
    async def transform(self, data: List[Any]):
        ...
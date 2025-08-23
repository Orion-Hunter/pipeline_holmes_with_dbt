from abc import ABC, abstractmethod
from typing import List, Any, Union

import pandas as pd


class ETLService(ABC):
    
    @abstractmethod
    async def extract(self, execution_rule: Any) -> Union[List[Any], None]:
        ...
    
    @abstractmethod
    async def load(self, data: List[Any], execution_rule: Any) -> None:
        ...
    
    @abstractmethod
    async def transform(self, data: List[Any]) -> Union[pd.DataFrame, None]:
        ...
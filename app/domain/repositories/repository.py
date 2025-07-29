from abc import ABC, abstractmethod
from datetime import date
from typing import Any, List


class Repository(ABC):
    
    @abstractmethod
    async def create(self, data: List[Any]) -> None:
        ...

    @abstractmethod
    async def get(self, id: str) -> object:
        ...
    
    @abstractmethod
    async def delete(self) -> None:
        ...
    
    @abstractmethod
    async def get_all(self) -> List[object]:
        ...
    
    @abstractmethod
    async def delete_by_interval(self, start_date: date, end_date: date) -> None:
        ...
    
    
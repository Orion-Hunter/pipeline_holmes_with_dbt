from datetime import date
from enum import Enum
from typing import Any
from dataclasses import dataclass

class PipelineExecutionType(Enum):
    APPEND= 'APPEND'
    FULL = 'FULL'
    REFRESH='REFRESH'
    
class PipelineExecutionStatus(Enum):
    SUCCESS='SUCCESS'
    ERROR = 'ERROR'

class ETLMethod(Enum):
    E = 'E'
    L = 'L'
    T = 'T'

class DataLayer(Enum):
    SILVER='SILVER'
    GOLD='GOLD'
    
@dataclass
class PipelinePayload:
    etl: str
    start_date: date
    end_date: date
    data_layer: DataLayer
    
@dataclass
class ResponsePayload:
    method: ETLMethod
    message: str

@dataclass
class BodyGroupTermFilter:
    name: str
    value: Any
    type: str
    filter: str
    field: str
    #label: str
    nested: bool
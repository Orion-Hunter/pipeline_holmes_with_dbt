from datetime import date
from enum import Enum
from dataclasses import dataclass

class PipelineExecutionType(Enum):
    BACKFILL = 'BACKFILL'
    APPEND= 'APPEND'
    FULL = 'FULL'
    
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
    
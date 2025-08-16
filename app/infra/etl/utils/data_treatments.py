import pandas as pd 
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def clean_string(value):
      return value.replace('\n', '').replace('\t', '') if value else value
                   
def safe_to_utc(dt):
    br_tz = ZoneInfo("America/Sao_Paulo")
    dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    timestamp_result = None
    if isinstance(dt, datetime):
        timestamp_result = dt.astimezone(br_tz)
        timestamp_result = timestamp_result.replace(microsecond=0, tzinfo=None)    
    print(timestamp_result)
    return timestamp_result 
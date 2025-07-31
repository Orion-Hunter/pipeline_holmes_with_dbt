import pandas as pd 
from datetime import datetime, timezone

def clean_string(value):
      return value.replace('\n', '').replace('\t', '') if value else value
                   
def safe_to_utc(dt):
    if dt is None or pd.isna(dt):
            return None
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    return None 
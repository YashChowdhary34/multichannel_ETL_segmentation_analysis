import pandas as pd

REF_SCHEMA = list(pd.read_csv("../../data/raw/online_retail.xlsx").columns)

def validate_schema(data: dict) -> bool:
  return (
    (set(data.keys()) == set(REF_SCHEMA)) and
    (len(data) == len(REF_SCHEMA))
  )


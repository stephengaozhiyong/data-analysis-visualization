from pydantic import BaseModel

class QueryForm(BaseModel):
    statement: str
    symbol: str

class QueryForm1(QueryForm):
    indicator: str
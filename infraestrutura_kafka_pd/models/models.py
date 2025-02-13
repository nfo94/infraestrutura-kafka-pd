from datetime import datetime

from pydantic import BaseModel


class Owner(BaseModel):
    email: str
    creator: str


class KafkaMessage(BaseModel):
    pk: int
    uid: str
    name: str
    version: str
    timestamp: datetime
    owner: Owner

class TransformedMessage(BaseModel):
    pk: int
    uid: str
    name: str
    version: str
    timestamp: datetime
    owner: Owner
    origin: str = "Consumer 2"
    company_name: str
    company_type: str

from pydantic import BaseModel


class Transaction(BaseModel):
    timestamp: int
    transaction_id: int
    user_id: int
    card_id: int
    site_id: int
    value: float
    location_id: int
    country: str

    def to_dict(self):
        return self.model_dump()

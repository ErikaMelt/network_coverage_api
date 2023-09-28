from pydantic import BaseModel


class ApiAdresseResponse(BaseModel):
    longitude: float
    latitude: float
    score: float

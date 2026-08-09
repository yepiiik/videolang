from pydantic import BaseModel


class Authentication(BaseModel):
    api_key: str
    
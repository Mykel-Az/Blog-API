from pydantic import BaseModel


class Aboutrequest(BaseModel):
    header: str
    body: str
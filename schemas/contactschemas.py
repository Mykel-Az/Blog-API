from pydantic import BaseModel, EmailStr
from typing import Annotated, Optional
from fastapi import Form
from datetime import datetime


class Contactrequest(BaseModel):
    name: Annotated[str, Form()]
    email: Annotated[EmailStr, Form()]
    subject: Annotated[str, Form()]
    message: Annotated[str, Form()]
    time: str



class Response(BaseModel):
    message: Optional [str] = None
    data : Optional [str | list | dict] = None


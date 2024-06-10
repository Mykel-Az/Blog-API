from pydantic import BaseModel, EmailStr
from typing import Optional, Annotated
from fastapi import Form

class UserBase(BaseModel):
    username: Annotated[str, Form()]
    first_name: Annotated[str, Form()]
    last_name: Annotated[str, Form()]
    email: Annotated[EmailStr, Form()]
    password: Annotated[str, Form()]
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class Response(BaseModel):
    message: Optional [str] = None
    data : Optional [str | list | dict] = None
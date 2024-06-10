from pydantic import BaseModel, NaiveDatetime
from datetime import datetime
from typing import Annotated, Optional
from fastapi import Body
from uuid import UUID



class BlogRequest(BaseModel):
    title: str
    body : str


class CreateBlog(BaseModel):
    title : str
    body : str
    first_name: str
    last_name: str
    time: str
    

class BlogUpdate(BaseModel):
    title: str
    body: str

class Response(BaseModel):
    message: Optional [str] = None
    data : Optional [str | dict | list] = None
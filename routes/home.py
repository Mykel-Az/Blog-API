from fastapi import APIRouter, status, HTTPException
from services.dbservices import db_dependency
from models import Blog
from schemas.blogschemas import Response


blogg = APIRouter()

@blogg.get("/blog_list", status_code=status.HTTP_200_OK)
async def blog_all(db: db_dependency):
    blog_list = db.query(Blog).all()
    return blog_list

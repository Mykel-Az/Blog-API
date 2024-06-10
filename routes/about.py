from fastapi import APIRouter, status, HTTPException, Path
from schemas.aboutschemas import Aboutrequest
from services.dbservices import db_dependency
from models import About
from datetime import datetime
from routes.user_auth import user_dependency

route = APIRouter()

# Endpoint to create an "About" article = Admin
@route.post("/write", status_code=status.HTTP_201_CREATED)
async def write_about(user: user_dependency, about: Aboutrequest, db: db_dependency):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    about_model = About(**about.model_dump(), time = datetime.now(), owner_id=user.get("id"))
    db.add(about_model)
    db.commit()

    return {"message": "About article saved"}


# Endpoint to view the "About" articles = Admin
@route.get("/display/", status_code=status.HTTP_200_OK)
async def about_display(user: user_dependency, db: db_dependency):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    about_list = db.query(About).all()
    return about_list


# Endpoint to edit an "About" article = Admin
@route.put("/edit/{about_id}", status_code=status.HTTP_201_CREATED)
async def update_about(request: Aboutrequest, user: user_dependency, db: db_dependency, about_id: int=Path(gt=0)):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    about_model = db.query(About).filter(About.id==about_id).filter(About.owner_id==user.get("id")).first()
    if about_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    request.header = about_model.header
    request.body = about_model.body

    db.add(about_model)
    db.commit()


# Endpoint to deleting an "About" article = Admin
@route.delete("/delete/{about_id}", status_code=status.HTTP_200_OK)
async def about_del(user: user_dependency, db: db_dependency, about_id: int=Path(gt=0)):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    about_model = db.query(About).filter(About.id==about_id).filter(About.owner_id==user.get("id")).first()
    if about_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist")
    
    db.delete(about_model)
    db.commit()

    return {"message": "deleted succesfully"}

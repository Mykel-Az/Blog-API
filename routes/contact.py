from fastapi import APIRouter, status, HTTPException, Path
from schemas.contactschemas import Contactrequest, Response
from services.dbservices import db_dependency
from models import Contact
from routes.user_auth import user_dependency
from datetime import datetime


route = APIRouter()

# Endpoint to create a contact
@route.post("/create", status_code=status.HTTP_201_CREATED)
async def create_contact(request: Contactrequest, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    contact_model = Contact(
        name = request.name,
        email = request.email,
        message = request.message,
        subject = request.subject,
        time = datetime.now(),
        owner_id = user.get("id")
        )
    db.add(contact_model)
    db.commit()

    return Response(message="Thank You, we will get back to you as soon as possible")


# Endpoint to check all contacts = Admin
@route.get("/display_all", status_code=status.HTTP_200_OK)
async def show_all(user: user_dependency, db: db_dependency):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    contact_list = db.query(Contact).all()
    return contact_list

# Endpoint to delete a contact = Admin
@route.delete("/del/{contact_id}", status_code=status.HTTP_200_OK)
async def delete(user: user_dependency, db: db_dependency, contact_id: int=Path(gt=0)):
    if user.get("role")!="Admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    contact_model = db.query(Contact).filter(Contact.id==contact_id).filter(Contact.owner_id==user.get("id")).first()
    if contact_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article doesn't exist")
    
    db.delete(contact_model)
    db.commit()

    return {"message": "deleted succesfully"}
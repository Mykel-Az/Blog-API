from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from services.dbservices import db_dependency
from schemas.userschemas import UserBase, Response, Token
from models import User
from typing import Annotated
from services.userservices import bcrpyt, authenticate_user, create_access_token, get_current_user
from datetime import timedelta

auth = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

#  Endpoint to create a user
@auth.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, user_request: UserBase):
    user_model = User(
        username = user_request.username,
        first_name = user_request.first_name,
        last_name = user_request.last_name,
        email = user_request.email,
        hashed_pasword = bcrpyt.hash(user_request.password),
        role = user_request.role,
        is_active = True
    )

    db.add(user_model)
    db.commit()

    return Response(message=f"Signup successfull, Welcome {user_request.first_name} You can now login as {user_request.username}")


# Endpoint for a user to signin
@auth.post("/login", response_model=Token)
async def login_access(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Authentication Failed"
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=10))

    return{
        "access_token": token,
        "token_type": "bearer"
    }
    

# Endpoint to view user detials
@auth.get("/userprofile/{user_id}", status_code=status.HTTP_200_OK)
async def userprofile(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Login to view your user profile")

    user_profile = db.query(User).filter(User.id == user.get("id")).first()
    if user_profile is not None:
        return user_profile
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="This doesn't exist or has not been created yet.")
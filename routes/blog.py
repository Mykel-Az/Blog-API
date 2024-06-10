from fastapi import APIRouter, status, HTTPException, Path, Request
from schemas.blogschemas import BlogRequest, CreateBlog, BlogUpdate, Response
from models import Blog, User
from services.dbservices import db_dependency
from routes.user_auth import user_dependency
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

blogg = APIRouter()

@blogg.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})




# Endpoint to create a blog
@blogg.post("/create", status_code=status.HTTP_201_CREATED)
async def write_blog(user: user_dependency, db: db_dependency, request: BlogRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    person = db.query(User).filter(User.id == user.get("id")).first()
    
    blog_model = Blog(
        title = request.title,
        body = request.body,
        first_name = person.first_name,
        last_name = person.last_name,
        time_posted = datetime.now(),
        owner_id = user.get("id")        
    )
   
    db.add(blog_model)
    db.commit()

    return {
        "title": blog_model.title,
        "body": blog_model.body,
        "Author": f"{blog_model.first_name} {blog_model.last_name}",
        "time": blog_model.time_posted
    }



# Endpoint to view blog
@blogg.get("/view/{blog_id}", status_code=status.HTTP_200_OK)
async def view_blog(blog_id: str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    myblog = db.query(Blog).filter(Blog.id==blog_id).filter(Blog.owner_id==user.get("id")).first()
    if myblog is not None:
        return myblog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# Endpoint to edit blog
@blogg.put("/edit/{blog_id}", status_code=status.HTTP_200_OK)
async def edit_blog(blog_id: str, user: user_dependency, db: db_dependency, request: BlogUpdate):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    myblog = db.query(Blog).filter(Blog.id==blog_id).filter(Blog.owner_id==user.get("id")).first()
    if myblog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    myblog.title = request.title
    myblog.body = request.body
    myblog.time_edited = datetime.now()
    myblog.edited = True

    db.add(myblog)
    db.commit()

    return {
        "title": myblog.title,
        "body": myblog.body,
        "Author": f"{myblog.first_name} {myblog.last_name}",
        "time": myblog.time_edited,
        "edited": True
    }


# Endpoint to delete a blog
@blogg.delete("/delete/{blog_id}", status_code=status.HTTP_200_OK)
async def delete_blog(blog_id:str, user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    myblog = db.query(Blog).filter(Blog.id==blog_id).filter(Blog.owner_id==user.get("id")).first()

    db.delete(myblog)
    db.commit()

    return Response(message="Blog deleted Successfully")

    



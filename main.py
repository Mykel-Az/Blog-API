from fastapi import FastAPI, Request, Form, status

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from routes.home import blogg as Homeroute
from routes.user_auth import auth as Authentication
from routes.blog import blogg as Blogroute
from routes.contact import route as Contactroute
from routes.about import route as Aboutroute

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(Homeroute, prefix="/Home", tags=["Home Page"])
app.include_router(Authentication, prefix="/auth", tags=["Authentication"])
app.include_router(Blogroute, prefix="/blog", tags=["Blog"])
app.include_router(Contactroute, prefix="/contact", tags=["Contacts"])
app.include_router(Aboutroute, prefix="/about", tags=["About"])


# @app.get("/")
# def loader():
#     return {"message": "Welcome to THE BLOG-API"}


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/add")
async def add(request: Request, name:str = Form(...)):
    print(name)
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


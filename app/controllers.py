from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from database import db
from database.models import User, Task

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)
 
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env 
 
def index(request: Request):
    return templates.TemplateResponse('index.html',{'request': request})

def admin(request: Request):
    return templates.TemplateResponse('admin.html', {'request': request, 'username': 'admin'})
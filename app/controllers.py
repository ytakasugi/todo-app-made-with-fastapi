from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request

from app.database import db
from app.database import models

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
    user = db.session.query(models.User).filter(models.User.username == 'admin').first()
    task = db.session.query(models.Task).filter(models.Task.user_id == user.id).all()
    db.session.close()
 
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})
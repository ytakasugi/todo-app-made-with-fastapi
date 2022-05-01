from datetime import datetime, timedelta

import re

from fastapi import FastAPI, Depends, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse

import db
from models import User, Task
from mycalendar import MyCalendar
from auth import auth

# 任意の4~20の英数字を示す正規表現
pattern = re.compile(r'\w{4,20}')
# 任意の6~20の英数字を示す正規表現
pattern_pw = re.compile(r'\w{6,20}')
# e-mailの正規表現
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)

security = HTTPBasic()
 
templates = Jinja2Templates(directory="../templates")
jinja_env = templates.env 
 
def index(request: Request):
    return templates.TemplateResponse('index.html',{'request': request})

def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)

    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    # 今日の日付と来週の日付
    today = datetime.now()
    next_w = today + timedelta(days=7)  # １週間後の日付

    """ [new] カレンダー関連 """
    # カレンダーをHTML形式で取得
    cal = MyCalendar(username,
                     {t.deadline.strftime('%Y%m%d'): t.done for t in task})  # 予定がある日付をキーとして渡す
    
    cal = cal.formatyear(today.year, 4)  # カレンダーをHTMLで取得

    # 直近のタスクだけでいいので、リストを書き換える
    task = [t for t in task if today <= t.deadline <= next_w]
    links = [t.deadline.strftime('/todo/'+username+'/%Y/%m/%d') for t in task]  # 直近の予定リンク


    # 特に問題がなければ管理者ページへ
    return templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'user': user,
            'task': task,
            'links': links,
            'calendar': cal
        }
    )

async def register(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse(
            'register.html',
            {
                'request': request,
                'username': '',
                'error': []
            }
        )

    if request.method == 'POST':
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        password_tmp = data.get('password_tmp')
        mail = data.get('mail')

        error = []

        tmp_user = db.session.query(User).filter(User.username == username).first()

        # エラー処理
        if tmp_user is not None:
            error.append('既に同じユーザが存在します。')
        if password != password_tmp:
            error.append('入力したパスワードが一致しません。')
        if pattern.match(username) is None:
            error.append('ユーザ名は4~20文字の半角英数字にしてください。')
        if pattern_pw.match(password) is None:
            error.append('パスワードは6~20文字の半角英数字にしてください。')
        if pattern_mail.match(mail) is None:
            error.append('正しくメールアドレスを入力してください。')

        # エラーがあれば、登録ページに戻す
        if error:
            return templates.TemplateResponse(
                'register.html',
                {
                    'request': request,
                    'username': username,
                    'error': error
                }
            )

        # エラーがなければ、ユーザを登録する
        user = User(username, password, mail)
        db.session.add(user)
        db.session.commit()
        db.session.close()

        return templates.TemplateResponse(
            'complete.html',
            {
                'request': request,
                'username': username
            }
        )

def detail(
    request: Request, 
    username,
    year,
    month,
    day,
    credentials: HTTPBasicCredentials = Depends(security)
):
    username_tmp = auth(credentials)

    # もし他のユーザが訪問してきたらはじく
    if username_tmp != username:
        return RedirectResponse('/')

    # ログインユーザを取得
    user = db.session.query(User).filter(User.username == username).first()
    # ログインユーザのタスクを取得
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    # 該当の日付と一致するものだけをリストする
    theday = '{}{}{}'.format(year, month.zfill(2), day.zfill(2))
    task = [t for t in task if t.deadline.strftime('%Y%m%d') == theday]

    return templates.TemplateResponse(
        'detail.html',
        {
            'request': request,
            'username':username,
            'task': task,
            'year': year,
            'month': month,
            'day': day
        }
    )

async def done(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証OK？
    username = auth(credentials)
 
    # ユーザ情報を取得
    user = db.session.query(User).filter(User.username == username).first()
 
    # ログインユーザのタスクを取得
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
 
    # フォームで受け取ったタスクの終了判定を見て内容を変更する
    data = await request.form()
    t_dones = data.getlist('done[]')  # リストとして取得
 
    for t in task:
        if str(t.id) in t_dones:  # もしIDが一致すれば "終了した予定" とする
            t.done = True
 
    db.session.commit()  # update!!
    db.session.close()
 
    return RedirectResponse('/admin') 

async def add(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    username = auth(credentials)

    # ユーザ情報を取得
    user = db.session.query(User).filter(User.username == username).first()

    # フォームからデータを取得
    data = await request.form()
    year = int(data['year'])
    month = int(data['month'])
    day = int(data['day'])
    hour = int(data['hour'])
    minute = int(data['minute'])

    deadline = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    # 新しくタスクを生成しコミット
    task = Task(user.id, data['content'], deadline)
    db.session.add(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse('/admin')

def delete(request: Request, t_id, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    username = auth(credentials)

    # ログインユーザー取得
    user = db.session.query(User).filter(User.username == username).first()

    # 該当タスクを取得
    task = db.session.query(Task).filter(Task.id == t_id).first()
    # もし、ユーザーIDが異なれば削除せずリダイレクト
    if task.user_id != user.id:
        return RedirectResponse('/admin')

    # 削除してコミット
    db.session.delete(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse('/admin')

def get(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    username = auth(credentials)

    # ユーザ情報を取得
    user = db.session.query(User).filter(User.username == username).first()

    # タスクを取得
    task = db.session.query(Task).filter(Task.user_id == user.id).all()

    db.session.close()

    # JSONフォーマット
    task = [{
        'id': t.id,
        'content': t.content,
        'deadline': t.deadline.strftime('%Y-%m-%d %H:%M:%S'),
        'published': t.date.strftime('%Y-%m-%d %H:%M:%S'),
        'done': t.done,
    } for t in task]

    return task


async def insert(request: Request,
                 content: str = Form(...), deadline: str = Form(...),
                 credentials: HTTPBasicCredentials = Depends(security)):
    """
    タスクを追加してJSONで新規タスクを返す。「deadline」は%Y-%m-%d_%H:%M:%S (e.g. 2019-11-03_12:30:00)の形式
    """
    # 認証
    username = auth(credentials)

    # ユーザ情報を取得
    user = db.session.query(User).filter(User.username == username).first()

    # タスクを追加
    task = Task(user.id, content, datetime.strptime(deadline, '%Y-%m-%d_%H:%M:%S'))

    db.session.add(task)
    db.session.commit()

    # テーブルから新しく追加したタスクを取得する
    task = db.session.query(Task).all()[-1]
    db.session.close()

    # 新規タスクをJSONで返す
    return {
        'id': task.id,
        'content': task.content,
        'deadline': task.deadline.strftime('%Y-%m-%d %H:%M:%S'),
        'published': task.date.strftime('%Y-%m-%d %H:%M:%S'),
        'done': task.done,
    }
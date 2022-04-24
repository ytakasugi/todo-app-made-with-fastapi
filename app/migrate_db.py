from models import *
from db import engine, session
import os

if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
        # テーブルを作成する
        Base.metadata.create_all(engine)

    # サンプルユーザを作成
    admin = User(username = 'admin', password = 'admin', mail = 'admin@example.com')
    session.add(admin)
    session.commit()

    # サンプルタスク
    task = Task(
        user_id = admin.id,
        content = 'Rustを仕事で使いたい',
        deadline = datetime.now(),
    )
    
    print(task)
    session.add(task)
    session.commit()

    # セッションのクローズ
    session.close()
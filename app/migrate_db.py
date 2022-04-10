from datetime import datetime

from models.model import SQLITE3_NAME, User, Task
from db import Base, session, engine
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
        deadline = datetime(2021, 12, 25, 12, 00, 00),
    )
    
    print(task)
    session.add(task)
    session.commit()

    # セッションのクローズ
    session.close()
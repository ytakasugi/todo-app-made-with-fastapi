import models
import db
import os

if __name__ == "__main__":
    path = models.SQLITE3_NAME
    if not os.path.isfile(path):
        # テーブルを作成する
        db.Base.metadata.create_all(db.engine)

    # サンプルユーザを作成
    admin = models.User(username = 'admin', password = 'admin', mail = 'admin@example.com')
    db.session.add(admin)
    db.session.commit()

    # サンプルタスク
    task = models.Task(
        user_id = admin.id,
        content = 'Rustを仕事で使いたい',
        deadline = models.datetime(2021, 12, 25, 12, 00, 00),
    )
    
    print(task)
    db.session.add(task)
    db.session.commit()

    # セッションのクローズ
    db.session.close()
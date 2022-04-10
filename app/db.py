from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ベースクラスを作成。これを継承してテーブルに対応するクラスを作成する。
Base = declarative_base()
RDB_PATH = 'sqlite:///db.sqlite3'
ECHO_LOG = True

# 接続用インスタンスの作成
engine = create_engine(
    RDB_PATH, echo=ECHO_LOG
)

Session = sessionmaker(bind=engine)
session = Session()
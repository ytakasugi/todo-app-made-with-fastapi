import calendar
from datetime import datetime

class MyCalendar(calendar.LocalHTMLCalendar):
    # コンストラクタ(イニシャライザ)
    # インスタンス作成時に必ず実行される特殊なメソッド
    def __init__(self, username, linked_date: dict):
        self.username = username
        self.linked_date = linked_date
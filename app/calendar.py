import calendar
from datetime import datetime

class MyCalendar(calendar.LocalHTMLCalendar):
    # コンストラクタ(イニシャライザ)
    # インスタンス作成時に必ず実行される特殊なメソッド
    def __init__(self, username, linked_date: dict):
        calendar.LocaleHTMLCalendar.__init__(self, firstweekday=6, locale='ja_jp')

        self.username = username
        self.linked_date = linked_date

    def formatmonth(self, theyear, themonth, withyear = True):
        # 空のリストを作成
        v = []
        # 以下のような使い方をすることで、リストに要素を追加する
        # ex. a(1) → リストvに要素1を追加
        a = v.append
        a('<table class="table table-bordered table-sm" style="table-layout: fixed;">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, theyear, themonth))  # ここも違う。年月日全て渡すようにする(後述)
            a('\n')
        a('</table><br>')
        a('\n')
        return ''.join(v)
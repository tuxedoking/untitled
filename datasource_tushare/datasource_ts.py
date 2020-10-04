import tushare as ts
from datetime import date
from datetime import timedelta


class Datasource:
    __TOKEN = '23f8e341c1130b8d3447d9a5e8d38a877fef1f9f16b67051db2ad361'

    def __init__(self):
        ts.set_token(self.__TOKEN)
        self.pro = ts.pro_api()

    def get_code_list(self):
        return self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    def get_dayline(self, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=5)
            start_date = (today-td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, adj='qfq', start_date=start_date, end_date=end_date)

    def get_weekline(self, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=35)
            start_date = (today - td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, freq='W', adj='qfq', start_date=start_date, end_date=end_date)

    def get_monthline(self, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=150)
            start_date = (today - td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, freq='M', adj='qfq', start_date=start_date, end_date=end_date)

    def get_todayline(self):
        return ts.get_today_all()

    def get_lasttradedays(self):
        today = date.today()
        end_date = '%d%02d%02d' % (today.year, today.month, today.day)
        df = self.pro.trade_cal(exchange='SSE', start_date='20200901', end_date=end_date)
        for row in df.itertuples():
            print(row)
        df = self.pro.trade_cal(exchange='SZSE', start_date='20200901', end_date=end_date)
        for row in df.itertuples():
            print(row)

'''
if __name__ == '__main__':
    ds = Datasource()
    df = ds.get_code_list()
    if df is None:
        print("get code list error")
    for row in df.itertuples():
        print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
'''

if __name__ == '__main__':
    ds = Datasource()
    print(ds.get_monthline())

'''
if __name__ == '__main__':
    ds = Datasource()
    df = ds.get_todayline()
    if df is None:
        print("get code list error")
    for row in df.itertuples():
        print(row)
'''
'''
if __name__ == '__main__':
    ds = Datasource()
    ds.get_lasttradedays()
'''
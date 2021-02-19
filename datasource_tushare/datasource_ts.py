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

    def get_code_list_kzz(self):
        return self.pro.cb_basic(fields="ts_code,bond_short_name,stk_code,stk_short_name,list_date,delist_date")

    @classmethod
    def get_day_line(cls, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=5)
            start_date = (today-td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, adj='qfq', start_date=start_date, end_date=end_date)

    @classmethod
    def get_week_line(cls, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=35)
            start_date = (today - td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, freq='W', adj='qfq', start_date=start_date, end_date=end_date)

    @classmethod
    def get_month_line(cls, code='000001.SZ', start_date=None, end_date=None):
        today = date.today()
        if start_date is None:
            td = timedelta(days=150)
            start_date = (today - td).strftime('%Y%m%d')
        if end_date is None:
            end_date = today.strftime('%Y%m%d')
        print(start_date, end_date)
        return ts.pro_bar(ts_code=code, freq='M', adj='qfq', start_date=start_date, end_date=end_date)

    @classmethod
    def get_today_line(cls):
        return ts.get_today_all()

    def get_last_trade_days(self):
        today = date.today()
        end_date = '%d%02d%02d' % (today.year, today.month, today.day)
        df = self.pro.trade_cal(exchange='SSE', start_date='20210201', end_date=end_date)
        last_date = 0
        d = {}
        for row in df.itertuples():
            if row.is_open == 1 and int(row.cal_date) > last_date:
                d['last_date'] = row.cal_date
            # print('SH', row.cal_date, row.is_open)
        return d
            #print('SZ', row2.cal_date, row2.is_open)


'''
if __name__ == '__main__':
    ds = Datasource()
    df = ds.get_code_list_kzz()
    if df is None:
        print("get code list error")
    for row in df.itertuples():
        print(row)
'''
'''
if __name__ == '__main__':
    ds = Datasource()
    df = ds.get_code_list()
    if df is None:
        print("get code list error")
    for row in df.itertuples():
        print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
'''
'''
if __name__ == '__main__':
    ds = Datasource()
    print(ds.get_monthline())
'''
'''
if __name__ == '__main__':
    ds = Datasource()
    df = ds.get_todayline()
    if df is None:
        print("get code list error")
    for row in df.itertuples():
        print(row)
'''

if __name__ == '__main__':
    ds = Datasource()
    print(ds.get_last_trade_days())

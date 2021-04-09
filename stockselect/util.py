import os
import dbm
import pickle
from datetime import date
from datetime import timedelta
import codetable
from ctypes import *


def is_zt(pre_close, close):
    d = (int(pre_close * 0.1 * 100 + 0.5)) / 100.0
    return int(close * 100 + 0.5) >= int((pre_close + d) * 100 + 0.5)


def get_zhang_fu(pre_close, close):
    return round(100*(close - pre_close)/pre_close, 2)


def get_last_day_line_close_price():
    d = {}
    try:
        db = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
        for key in db.keys():
            data = db[key]
            lines = pickle.loads(data)
            code = bytes.decode(key)
            for date in sorted(lines, reverse=True):
                d[code] = (date, lines[date]['raw'][3])
                break
        db.close()
    except Exception as err2:
        print(err2)
    finally:
        pass
    return d


def get_start_date():
    today = date.today()
    td = timedelta(days=100)
    start_date = (today - td).strftime('%Y%m%d')
    return int(start_date)


def get_start_date_month_line():
    today = date.today()
    td = timedelta(days=100*3)
    start_date = (today - td).strftime('%Y%m%d')
    return int(start_date)


def get_start_date_week_line():
    today = date.today()
    td = timedelta(days=100*2)
    start_date = (today - td).strftime('%Y%m%d')
    return int(start_date)


def get_work_area():
    class RECT(Structure):
        _fields_ = [("left", c_long),
                    ("top", c_long),
                    ("right", c_long),
                    ("bottom", c_long)]

    r = RECT()
    pr = pointer(r)
    user32 = windll.user32
    if user32.SystemParametersInfoA(0x0030, 0, pr, 0) == 0:
        return None
    return pr.contents.left, pr.contents.top, pr.contents.right, pr.contents.bottom


def find_ths_wnd():
    class HWND(Structure):
        _fields_ = [("unused", c_int)]
    user32 = windll.user32
    handle = HWND()
    handle.unused = 0
    handle_pr = pointer(handle)
    handle_pr = user32.FindWindowExW(0, 0, 0, 0)
    print(handle_pr)
    #print(handle_pr.contents)


code_table = None


def get_stock_name(code):
    try:
        global code_table
        if code_table is None:
            print('loading code table...')
            code_table = codetable.read_codetable(os.getcwd() + '/../dbms/codetable.dbm')
            print('load code table ok')
        if code not in code_table:
            return ''
        else:
            return code_table[code]
    except Exception as err:
        print(err)
        return ''


__end_date = 20500101

if __name__ == '__main__':
    find_ths_wnd()
    # a = get_work_area()
    # print(type(a))
    # print(get_stock_name('002531.SZ'))
    # print(get_start_date_month_line())
    # print(type(get_start_date()))
    # print(get_last_day_line_close_price())
    # print(is_zt(3.35, 3.69))

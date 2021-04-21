import os
import dbm
import pickle
from datetime import date
from datetime import timedelta
from ctypes import *
import win32api
import win32con
import win32gui
import win32process
import time
import datasource_tushare.datasource_ts as dsts


def is_zt(pre_close, close):
    d = (int(pre_close * 0.1 * 100 + 0.5)) / 100.0
    return int(close * 100 + 0.5) >= int((pre_close + d) * 100 + 0.5)


def get_zhang_fu(pre_close, close):
    return round(100 * (close - pre_close) / pre_close, 2)


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
    td = timedelta(days=100 * 3)
    start_date = (today - td).strftime('%Y%m%d')
    return int(start_date)


def get_start_date_week_line():
    today = date.today()
    td = timedelta(days=100 * 2)
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
    hwnd_ths = 0
    while True:
        hwnd_ths = win32gui.FindWindowEx(None, hwnd_ths, None, None)
        if hwnd_ths == 0:
            return False
        if win32gui.IsWindowVisible(hwnd_ths):
            win_text = win32gui.GetWindowText(hwnd_ths)
            if win_text[0:3] == '同花顺':
                return hwnd_ths
    return False


def press_code_on_ths(hwnd_ths, code='002531'):
    win32gui.PostMessage(hwnd_ths, win32con.WM_KEYDOWN, ord('6') & 0xFF, 0)
    win32gui.PostMessage(hwnd_ths, win32con.WM_KEYUP, ord('6') & 0xFF, 0)
    time.sleep(0.3)
    win32gui.SetForegroundWindow(hwnd_ths)
    self_thread_id = win32api.GetCurrentThreadId()
    fore_thread_id = win32process.GetWindowThreadProcessId(hwnd_ths)
    win32process.AttachThreadInput(fore_thread_id[0], self_thread_id, True)
    obj_wnd = win32gui.GetFocus()
    win32gui.SendMessage(obj_wnd, win32con.WM_SETTEXT, 0, code)
    win32gui.PostMessage(obj_wnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.PostMessage(obj_wnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    win32process.AttachThreadInput(fore_thread_id[0], self_thread_id, False)
    return True


code_table = None


def get_stock_name(code):
    global code_table
    try:
        if code_table is None:
            code_table = {}
            ds = dsts.Datasource()
            df = ds.get_code_list()
            for index in df.index:
                code_table[df.loc[index, 'ts_code']] = df.loc[index, 'name']
        if code not in code_table:
            return ''
        else:
            return code_table[code]
    except Exception as err:
        print(err)
        return ''


__end_date = 20500101

if __name__ == '__main__':
    # print(get_stock_name('002351.SZ'))
    # print(get_stock_name('601598.SH'))
    # print(get_stock_name('002531.SZ'))
    hwnd = find_ths_wnd()
    if hwnd == False:
        exit(0)
    else:
        press_code_on_ths(hwnd)

    # a = get_work_area()
    # print(type(a))
    # print(get_stock_name('002531.SZ'))
    # print(get_start_date_month_line())
    # print(type(get_start_date()))
    # print(get_last_day_line_close_price())
    # print(is_zt(3.35, 3.69))

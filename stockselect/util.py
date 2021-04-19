import os
import dbm
import pickle
from datetime import date
from datetime import timedelta
import codetable
from ctypes import *
import win32api
import win32con
import win32gui
import win32process
import time
import pandas as pd
import numpy as np
import datasource_tushare.datasource_ts as dsts


def is_zt(pre_close, close):
    d = (int(pre_close * 0.1 * 100 + 0.5)) / 100.0
    return int(close * 100 + 0.5) >= int((pre_close + d) * 100 + 0.5)


def get_zhang_fu(pre_close, close):
    return round(100 * (close - pre_close) / pre_close, 2)

'''
__last_t = 0
periods = (5, 10, 20, 30, 60, 120, 250)


def cal_pma_s_in_data_frame(df_day_line):
    t = time.time()
    l4df = []
    close_array = np.array(df_day_line['close'])
    for i, close in enumerate(close_array):
        d = {}
        for period in periods:
            if i + period > len(df_day_line):
                d[f'pma{period}'] = np.nan
            else:
                a = close_array[i:i + period]
                d[f'pma{period}'] = np.sum(a) / len(a)
        l4df.append(d)
    print('cal pma s', time.time() - t)
    return pd.concat([df_day_line, pd.DataFrame(l4df)], axis=1)


def get_lines_from_net(ts_code, start_date, get_lines_from_net_fun_name, interval=0):
    global __last_t
    if interval > 0:
        interval_last = time.time() - __last_t
        if interval_last < interval:
            time.sleep(interval_last)
            print('sleep ', interval_last)
        __last_t = time.time()

    df_from_net = get_lines_from_net_fun_name(ts_code, start_date=start_date)
    if df_from_net is None or len(df_from_net) == 0:
        return None
    return df_from_net.dropna(subset=['close']).set_index('trade_date')


def put_lines_from_net_to_dbm(file_name, get_lines_from_net_fun_name, interval=0):
    try:
        db = dbm.open(file_name, 'c')
        ds = Datasource()
        df = ds.get_code_list()

        start_date_before_100 = ds.get_last_n_trade_days(20)

        last_t = 0
        for index in df.index:
            ts_code = df.loc[index, 'ts_code']
            print(ts_code)

            data = db.get(ts_code)
            if data is None:
                print('dbm里没有')
                df_from_net = get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name, interval)
                if df_from_net is None:
                    continue
                # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                # if df_from_net is None or len(df_from_net) == 0:
                #     continue
                # df_from_net = df_from_net.dropna(subset=['close'])
                df_result = cal_pma_s_in_data_frame(df_from_net)
                print(df_result)
                db[ts_code] = pickle.dumps(df_result)
            else:
                df_dbm = pickle.loads(data)

                df_from_net = get_lines_from_net(ts_code, start_date_before_100, get_lines_from_net_fun_name, interval)
                if df_from_net is None:
                    continue
                # df_from_net = get_lines_from_net_fun_name(ts_code, start_date=start_date_before_100)
                # if df_from_net is None or len(df_from_net) == 0:
                #     continue
                # df_from_net = df_from_net.dropna(subset=['close'])

                # trade_date1 = df_from_net.loc[df_from_net.index[df_from_net.shape[0] - 1], 'trade_date']
                # trade_date2 = df_dbm.loc[0, 'trade_date']
                trade_date1 = df_from_net.index[-1]
                trade_date2 = df_dbm.index[0]
                print('last date in net dataframe = ', trade_date1)
                print('first date in dbm dataframe = ', trade_date2)
                if trade_date1 > trade_date2:
                    df_from_net = get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name, interval)
                    if df_from_net is None:
                        continue
                    # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                    # if df_from_net is None or len(df_from_net) == 0:
                    #     continue
                    # df_from_net = df_from_net.dropna(subset=['close'])
                    df_result = cal_pma_s_in_data_frame(df_from_net)
                    print(df_result)
                    db[ts_code] = pickle.dumps(df_result)
                else:
                    db_merge = merge_lines(df_from_net, df_dbm)
                    # db_merge = merge_lines(df_from_net, df_dbm.drop([0, 1]))
                    if db_merge is None:
                        print('除权啦')
                        df_from_net = get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name, interval)
                        if df_from_net is None:
                            continue
                        # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                        # if df_from_net is None or len(df_from_net) == 0:
                        #     continue
                        # df_from_net = df_from_net.dropna(subset=['close'])
                        df_result = cal_pma_s_in_data_frame(df_from_net)
                        print(df_result)
                        db[ts_code] = pickle.dumps(df_result)
                    elif db_merge is df_dbm:
                        print('dbm里是全的')
                        pass
                    else:
                        print(db_merge)
                        db[ts_code] = pickle.dumps(db_merge)
    except Exception as err:
        print(err)
    finally:
        db.close()


def merge_lines(df_net, df_dbm):
    i = 0
    for i, index in enumerate(df_net.index):
        if index == df_dbm.index[0]:
            if df_net.loc[index, 'open'] == df_dbm.loc[df_dbm.index[0], 'open'] \
                    and df_net.loc[index, 'high'] == df_dbm.loc[df_dbm.index[0], 'high'] \
                    and df_net.loc[index, 'low'] == df_dbm.loc[df_dbm.index[0], 'low'] \
                    and df_net.loc[index, 'close'] == df_dbm.loc[df_dbm.index[0], 'close']:
                break
            else:
                return None
        # if df_net.loc[index, 'trade_date'] == df_dbm.loc[df_dbm.index[0], 'trade_date']:
        #     if df_net.loc[index, 'open'] == df_dbm.loc[df_dbm.index[0], 'open'] \
        #             and df_net.loc[index, 'high'] == df_dbm.loc[df_dbm.index[0], 'high'] \
        #             and df_net.loc[index, 'low'] == df_dbm.loc[df_dbm.index[0], 'low'] \
        #             and df_net.loc[index, 'close'] == df_dbm.loc[df_dbm.index[0], 'close']:
        #         break
        #     else:
        #         return None
    if i == 0:
        return df_dbm

    print(f'新增{index}条记录')
    df_up = df_net.iloc[0:i]
    close_array = np.append(np.array(df_up['close']), np.array(df_dbm['close']))

    l4df = []
    for i, index in enumerate(df_up.index):
        d = {}
        for period in periods:
            if i + period > len(close_array):
                d[f'pma{period}'] = np.nan
            else:
                a = close_array[i:i + period]
                d[f'pma{period}'] = np.sum(a) / len(a)
        l4df.append(d)

    df_up2 = pd.concat([df_up, pd.DataFrame(l4df, index=df_up.index)], axis=1)
    print(df_up2)
    return pd.concat([df_up2, df_dbm], axis=0)
    # return pd.concat([df_up2, df_dbm], axis=0).reset_index(drop=True)
'''


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

import dbm
import pickle
import os
import sys
import time

import numpy as np
import pandas as pd


def cal_pmas(lines):
    pmas = []
    for date in sorted(lines):
        close = lines[date]['raw'][3]
        pmas.append(close)
        if len(pmas) >= 5:
            lines[date]['pma5'] = sum(pmas[-5:]) / 5
        if len(pmas) >= 10:
            lines[date]['pma10'] = sum(pmas[-10:]) / 10
        if len(pmas) >= 20:
            lines[date]['pma20'] = sum(pmas[-20:]) / 20
        if len(pmas) >= 30:
            lines[date]['pma30'] = sum(pmas[-30:]) / 30
        if len(pmas) >= 60:
            lines[date]['pma60'] = sum(pmas[-60:]) / 60
        if len(pmas) >= 120:
            lines[date]['pma120'] = sum(pmas[-120:]) / 120
        if len(pmas) >= 250:
            lines[date]['pma250'] = sum(pmas[-250:]) / 250


def cal_pma_s_in_data_frame(close_series, counts):
    t = time.time()
    # df = pd.DataFrame()
    l = []
    # for i, index in enumerate(close_series.index):
    for i in range(len(close_series)):
        d = {}
        for count in counts:
            if i + count > len(close_series):
                d[f'pma{count}'] = np.nan
            else:
                s = close_series[i:i + count - 1]
                d[f'pma{count}'] = np.sum(s)/len(s) #np.average()
        l.append(d)
    df = pd.DataFrame(l)
    print('cal pma s', time.time() - t)
    # print(df)
    return df


if __name__ == '__main__':
    try:
        pd.set_option('display.max_columns', 1000)
        db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        for key in db.keys():
            data = db[key]
            code = bytes.decode(key)
            df = pickle.loads(data)
            cal_pma_s_in_data_frame(df, [5, 10, 20, 30, 60, 120, 250])
            print(df)
    except Exception as err:
        print(err)
    finally:
        db.close()

'''
def cal_pma_bolang(lines, str_='250'):
    str = 'pma' + str_
    fromdate = 0
    lastdate = 0
    qushi = -1  #-1趋势不明　1-趋势上升　2-趋势下降
    count = 0
    ret = []

    for date in sorted(lines):
        if str not in lines[date]:
            continue
        else:
            pma = lines[date][str]
            if fromdate == 0:
                fromdate = date
                qushi = -1
                lastpma = pma
                lastdate = date
                continue
            if qushi == -1:
                if pma > lastpma:
                    qushi = 1
                    count = 1
                elif pma < lastpma:
                    qushi = 2
                    count = 1
                elif pma == lastpma:
                    fromdate = date
                lastpma = pma
                lastdate = date
            if qushi == 1:
                if pma >= lastpma:
                    count += 1
                    pass
                elif pma < lastpma:
                    t = (fromdate, lastdate, qushi, count)
                    ret.append(t)
                    fromdate = date
                    qushi = 2
                    count = 1
                lastpma = pma
                lastdate = date
            if qushi == 2:
                if pma <= lastpma:
                    count += 1
                    pass
                elif pma > lastpma:
                    t = (fromdate, lastdate, qushi, count)
                    ret.append(t)
                    fromdate = date
                    qushi = 1
                    count = 1
                lastpma = pma
                lastdate = date
    return ret

'''
'''
if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/dayline.dbm')
        for key in db.keys():
            print(key)
            data = db[key]
            daylines = json.loads(data)
            cal_pmas(daylines)
            db[key] = json.dumps(daylines)
            #code = bytes.decode(key)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
'''
'''
if __name__ == '__main__':
    try:
        print(os.getcwd())
        db = dbm.open(os.getcwd() + '/dbms/dayline.dbm')
        for key in db.keys():
            data = db[key]
            code = bytes.decode(key)
            print(code)
            #if code == '600549.SH':
            #    iii = 999
            daylines = pickle.loads(data)
            pmabolangs = cal_pma_bolang(daylines)
            print(pmabolangs)
        db.close()
    except Exception as err:
        s = sys.exc_info()
        print(err, s[2].tb_lineno)
    finally:
        pass
'''

# def cal_pma_s_in_data_frame2(close_series, count):
#     t = time.time()
#     df = pd.DataFrame()
#     for index in close_series.index:
#         index2 = index
#         sum2 = 0
#         s = set(count)
#
#         for i, index2 in enumerate(close_series.index, 1):
#             sum2 += close_series.loc[index2]
#             if i in s:
#                 # df.loc[index, f'pma{i}'] = sum2 / i
#                 haha = sum2 / i
#                 s.discard(i)
#                 if len(s) == 0:
#                     break
#         for i in s:
#             pass
#             # df.loc[index, f'pma{i}'] = np.nan
#     print('cal pma s', time.time()-t)

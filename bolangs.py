import dbm
import os
import pickle

if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        for key in db.keys():
            data = db[key]
            lines = pickle.loads(data)
            code = bytes.decode(key)
            if len(lines) < 30:
                continue
            qu_shi = 0
            bo_lang_s = []
            nz_count = 0
            dates = sorted(lines.keys())
            qu_shi_from_date = dates[0]
            qu_shi_to_date = dates[0]
            del(dates[0])

            for date in dates:
                close = lines[date]['raw'][3]
                if close < lines[qu_shi_to_date]['raw'][3]:
                    if qu_shi == 2:
                        qu_shi_to_date = date
                        nz_count = 0
                    elif qu_shi == 1:
                        nz_count += 1
                        if nz_count >= 5:
                            bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date, 'qu_shi': qu_shi}    # 前闭后开,如：[20200301,20200401)
                            bo_lang_s.append(bo_lang)
                            qu_shi_from_date = qu_shi_to_date
                            qu_shi_to_date = date
                            qu_shi = 2
                            nz_count = 0
                    elif qu_shi == 0:
                        qu_shi = 2
                        qu_shi_to_date = date
                        nz_count = 0
                else:
                    if qu_shi == 1:
                        qu_shi_to_date = date
                        nz_count = 0
                    elif qu_shi == 2:
                        nz_count += 1
                        if nz_count >= 5:
                            bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date, 'qu_shi': qu_shi}    # 前闭后开，如：[20200301,20200401)
                            bo_lang_s.append(bo_lang)
                            qu_shi_from_date = qu_shi_to_date
                            qu_shi_to_date = date
                            qu_shi = 1
                            nz_count = 0
                    elif qu_shi == 0:
                        qu_shi = 1
                        qu_shi_to_date = date
                        nz_count = 0

            bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date, 'qu_shi': qu_shi}
            bo_lang_s.append(bo_lang)

            if qu_shi_to_date < dates[-1]:
                bo_lang = {'from': qu_shi_to_date, 'to': dates[-1], 'qu_shi': 2 if qu_shi == 1 else 1}
                bo_lang_s.append(bo_lang)

        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

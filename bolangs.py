import dbm
import os
import pickle


def cal_bo_lang_s(lines):
    qu_shi = 0
    bo_lang_s = []
    nz_count = 0
    dates = sorted(lines.keys())
    qu_shi_from_date = dates[0]
    qu_shi_to_date = dates[0]
    del (dates[0])

    for date in dates:
        close = lines[date]['raw'][3]
        if close < lines[qu_shi_to_date]['raw'][3]:
            if qu_shi == 2:
                qu_shi_to_date = date
                nz_count = 0
            elif qu_shi == 1:
                nz_count += 1
                if nz_count >= 5:
                    bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date,
                               'qu_shi': '上' if qu_shi == 1 else '下'}  # 前闭后开,如：[20200301,20200401)
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
                    bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date,
                               'qu_shi': '上' if qu_shi == 1 else '下'}  # 前闭后开，如：[20200301,20200401)
                    bo_lang_s.append(bo_lang)
                    qu_shi_from_date = qu_shi_to_date
                    qu_shi_to_date = date
                    qu_shi = 1
                    nz_count = 0
            elif qu_shi == 0:
                qu_shi = 1
                qu_shi_to_date = date
                nz_count = 0

    bo_lang = {'from': qu_shi_from_date, 'to': qu_shi_to_date, 'qu_shi': '上' if qu_shi == 1 else '下'}
    bo_lang_s.append(bo_lang)

    if qu_shi_to_date < dates[-1]:
        bo_lang = {'from': qu_shi_to_date, 'to': dates[-1], 'qu_shi': '下' if qu_shi == 1 else '上'}
        bo_lang_s.append(bo_lang)

    return bo_lang_s


if __name__ == '__main__':
    try:
        db_bo_lang_s = dbm.open(os.getcwd() + '/dbms/day_line_bo_lang_s.dbm', 'c')
        db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        for key in db.keys():
            data = db[key]
            lines2 = pickle.loads(data)
            code = bytes.decode(key)
            # if len(lines2) < 30:
            #     continue
            bo_lang_s2 = cal_bo_lang_s(lines2)
            print(code, bo_lang_s2)
            db_bo_lang_s[code] = pickle.dumps(bo_lang_s2)
        db.close()
        db_bo_lang_s.close()
    except Exception as err:
        print(err)
    finally:
        pass

import dbm
import os
import pickle


# dates和values都是np.array对象
def cal_bo_lang_s2(dates, values):
    if len(dates) != len(values):
        return None
    if len(values) <= 1:
        return None

    qu_shi = 0
    bo_lang_s = []
    nz_count = 0
    qu_shi_from_index = 0
    qu_shi_to_index = 0
    i = qu_shi_to_index + 1

    while i < len(dates):
        value = values[i]
        if value < values[qu_shi_to_index]:
            if qu_shi == 2:
                qu_shi_to_index = i
                nz_count = 0
            elif qu_shi == 1:
                nz_count += 1
                if nz_count >= 5:
                    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
                               'from_value': values[qu_shi_from_index], 'to_value': values[qu_shi_to_index],
                               'qu_shi': '上' if qu_shi == 1 else '下'}
                    bo_lang_s.append(bo_lang)
                    qu_shi_from_index = qu_shi_to_index
                    qu_shi_to_index = qu_shi_to_index
                    i = qu_shi_to_index + 1
                    qu_shi = 2
                    nz_count = 0
                    continue
            elif qu_shi == 0:
                qu_shi = 2
                qu_shi_to_index = i
                nz_count = 0
        else:
            if qu_shi == 1:
                qu_shi_to_index = i
                nz_count = 0
            elif qu_shi == 2:
                nz_count += 1
                if nz_count >= 5:
                    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
                               'from_value': values[qu_shi_from_index], 'to_value': values[qu_shi_to_index],
                               'qu_shi': '上' if qu_shi == 1 else '下'}
                    bo_lang_s.append(bo_lang)
                    qu_shi_from_index = qu_shi_to_index
                    qu_shi_to_index = qu_shi_to_index
                    i = qu_shi_to_index + 1
                    qu_shi = 1
                    nz_count = 0
                    continue
            elif qu_shi == 0:
                qu_shi = 1
                qu_shi_to_index = i
                nz_count = 0
        i += 1

    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
               'from_value': values[qu_shi_from_index], 'to_value': values[qu_shi_to_index],
               'qu_shi': '上' if qu_shi == 1 else '下'}
    bo_lang_s.append(bo_lang)

    if qu_shi_to_index < len(dates) - 1:
        bo_lang = {'from': dates[qu_shi_to_index], 'to': dates[-1],
                   'from_value': values[qu_shi_to_index], 'to_value': values[-1],
                   'qu_shi': '下' if qu_shi == 1 else '上'}
        bo_lang_s.append(bo_lang)

    return bo_lang_s


def cal_bo_lang_s_from_lines_dbm_to_bo_lang_s_dbm(file_name_lines, file_name_bo_lang_s):
    try:
        db_day_line_bo_lang_s = dbm.open(file_name_bo_lang_s, 'c')
        db = dbm.open(file_name_lines)
        for key in db.keys():
            data = db[key]
            df = pickle.loads(data)
            code = bytes.decode(key)

            dates = list(reversed(df.index))
            values = list(reversed(df['close']))
            bo_lang_s2 = cal_bo_lang_s2(dates, values)

            if bo_lang_s2 is None:
                continue

            print(code, bo_lang_s2)
            db_day_line_bo_lang_s[code] = pickle.dumps(bo_lang_s2)
        db.close()
        db_day_line_bo_lang_s.close()
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    try:
        db = dbm.open('E:/dbms/day_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        # print(db.get(';a;a'))
        for key in db.keys():
            data = db[key]
            df = pickle.loads(data)
            code = bytes.decode(key)
            print(code)
            dates = list(reversed(df.index))
            values = list(reversed(df['close']))
            print(cal_bo_lang_s2(dates, values))
            # print(df)

    except Exception as err:
        print(err)
    finally:
        db.close()

'''
def cal_bo_lang_s(lines):
    if len(lines) <= 1:
        return None
    qu_shi = 0
    bo_lang_s = []
    nz_count = 0
    dates = sorted(lines.keys())
    qu_shi_from_index = 0
    qu_shi_to_index = 0
    i = qu_shi_to_index + 1

    while i < len(dates):
        close = lines[dates[i]]['raw'][3]
        if close < lines[dates[qu_shi_to_index]]['raw'][3]:
            if qu_shi == 2:
                qu_shi_to_index = i
                nz_count = 0
            elif qu_shi == 1:
                nz_count += 1
                if nz_count >= 5:
                    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
                               'qu_shi': '上' if qu_shi == 1 else '下'}
                    bo_lang_s.append(bo_lang)
                    qu_shi_from_index = qu_shi_to_index
                    qu_shi_to_index = qu_shi_to_index
                    i = qu_shi_to_index + 1
                    qu_shi = 2
                    nz_count = 0
                    continue
            elif qu_shi == 0:
                qu_shi = 2
                qu_shi_to_index = i
                nz_count = 0
        else:
            if qu_shi == 1:
                qu_shi_to_index = i
                nz_count = 0
            elif qu_shi == 2:
                nz_count += 1
                if nz_count >= 5:
                    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
                               'qu_shi': '上' if qu_shi == 1 else '下'}
                    bo_lang_s.append(bo_lang)
                    qu_shi_from_index = qu_shi_to_index
                    qu_shi_to_index = qu_shi_to_index
                    i = qu_shi_to_index + 1
                    qu_shi = 1
                    nz_count = 0
                    continue
            elif qu_shi == 0:
                qu_shi = 1
                qu_shi_to_index = i
                nz_count = 0
        i += 1

    bo_lang = {'from': dates[qu_shi_from_index], 'to': dates[qu_shi_to_index],
               'qu_shi': '上' if qu_shi == 1 else '下'}
    bo_lang_s.append(bo_lang)

    if qu_shi_to_index < len(dates) - 1:
        bo_lang = {'from': dates[qu_shi_to_index], 'to': dates[-1],
                   'qu_shi': '下' if qu_shi == 1 else '上'}
        bo_lang_s.append(bo_lang)

    return bo_lang_s
'''

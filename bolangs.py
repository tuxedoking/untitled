import dbm
import os
import pickle


def cal_bo_lang_s(lines):
    if len(lines) <= 1:
        return None
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


def cal_bo_lang_s2(lines):
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
                               'qu_shi': '上' if qu_shi == 1 else '下'}  # 前闭后开,如：[20200301,20200401)
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
                               'qu_shi': '上' if qu_shi == 1 else '下'}  # 前闭后开，如：[20200301,20200401)
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

    return bo_lang_s

import dbm
import pickle
import os
from stockselect import util

result_cache = {}


def select(db, start_date, max_day_count=50):
    try:
        items = []
        cache_key = __file__ + start_date + str(max_day_count)
        global result_cache
        if cache_key in result_cache:
            return result_cache[cache_key]

        for key in db.keys():
            data = db[key]
            df_lines = pickle.loads(data)
            code = bytes.decode(key)
            # close_series = df_lines[df_lines.index >= start_date]['close']
            close_series = df_lines['close']
            flag = False
            for i, date in enumerate(close_series.index):
                if date < start_date:
                    break
                if flag:
                    break
                # close = df_lines.loc[date, 'close']
                close = close_series[date]
                # for count, j in enumerate(range(i + 1, len(df_lines)), 1):
                for count, j in enumerate(range(i + 1, len(close_series)), 1):
                    # if df_lines.loc[df_lines.index[j], 'close'] > close:
                    if close_series[j] > close:
                        if count > max_day_count:
                            item = (date, code, util.get_stock_name(code), count)
                            items.append(item)
                            print(item)
                            # tv.insert('', tvi, values=item)
                            # tvi += 1
                            # if tvi > 10:
                            #     return
                            flag = True
                            break
                        else:
                            break
        result_cache[cache_key] = items
        return items
    except Exception as err:
        print(err)
        return None


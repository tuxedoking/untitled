import dbm
import pickle
import os
from stockselect import util


def select(db, tv, start_date, max_day_count=50):
    try:
        # file_name = os.getcwd() + '/dbms/day_line.dbm'
        # db = dbm.open(file_name)
        tvi = 0
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
                            print(item)
                            tv.insert('', tvi, values=item)
                            tvi += 1
                            flag = True
                            break
                        else:
                            break
    except Exception as err:
        print(err)
    finally:
        # db.close()
        pass


if __name__ == '__main__':
    select(tv=None, start_date='20210101')

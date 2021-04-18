import dbm
import pickle
import os
from util import get_stock_name

MAX_DAY_COUNT = 50


def select(tv, start_date):
    try:
        db = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
        for key in db.keys():
            data = db[key]
            df_lines = pickle.loads(data)
            code = bytes.decode(key)
            close_series = df_lines[df_lines.index >= start_date]['close']
            for i, date in enumerate(close_series.index):
                close = close_series[date]
                for j in range(i, len(close_series)):
            # count = 0
            # for date in sorted(lines, reverse=True):
            #     if int(date) > end_date:
            #         continue
            #     elif start_date <= int(date) <= end_date:
            #         to_date = int(date)
            #         to_close = lines[date]['raw'][3]
            #         for date2 in sorted(lines, reverse=True):
            #             if date2 >= date:
            #                 continue
            #             else:
            #                 if lines[date2]['raw'][3] < to_close:
            #                     count += 1
            #                 else:
            #                     if count > MAX_DAY_COUNT:
            #                         result_row = [to_date, code[0:6], get_stock_name(code), count]
            #                         print(result_row)
            #                     break
            #         if count > MAX_DAY_COUNT:
            #             break
            #     elif int(date) < start_date:
            #         break
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    select()

from datasource_tushare import datasource_ts as ds_ts
import pmas
from math import isnan
import dbm
import pickle
import os
import sys


if __name__ == '__main__':
    try:
        start_date = None
        # start_date = '20210201'
        # start_date = '19800101'
        if len(sys.argv) > 1 and sys.argv[1] == 'schedule_task':
            start_date = '19800101'

        db = dbm.open(os.getcwd() + '/dbms/day_line.dbm', 'c')
        ds = ds_ts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            day_lines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                day_lines = pickle.loads(data)

            df2 = ds.get_day_line(row.ts_code, start_date=start_date)
            if df2 is None:
                continue
            for row2 in df2.itertuples():
                print(row2)
                if isnan(row2.close):
                    continue
                if row2.trade_date not in day_lines:
                    day_lines[row2.trade_date] = {}
                    day_lines[row2.trade_date]['raw'] = [row2.open, row2.high, row2.low, row2.close, row2.pre_close,
                                                         row2.vol, row2.amount]

            pmas.cal_pmas(day_lines)
            db[row.ts_code] = pickle.dumps(day_lines)

        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

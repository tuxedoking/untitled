from datasource_tushare import datasource_ts as ds_ts
import pmas
from math import isnan
import dbm
import pickle
import os
import sys
import time


if __name__ == '__main__':
    try:
        # start_date = None
        # start_date = '20210201'
        start_date = '19800101'
        if len(sys.argv) > 1 and sys.argv[1] == 'schedule_task':
            start_date = '19800101'

        db = dbm.open(os.getcwd() + '/dbms/week_line.dbm', 'c')
        ds = ds_ts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            week_lines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                week_lines = pickle.loads(data)

            # df2 = ds.get_week_line(row.ts_code)
            df2 = ds.get_week_line(row.ts_code, start_date=start_date)
            time.sleep(0.1)
            if df2 is None:
                continue
            for row2 in df2.itertuples():
                print(row2)
                if isnan(row2.close):
                    continue
                if row2.trade_date not in week_lines:
                    week_lines[row2.trade_date] = {}
                    week_lines[row2.trade_date]['raw'] = [row2.open, row2.high, row2.low, row2.close, row2.pre_close,
                                                          row2.vol, row2.amount]

            pmas.cal_pmas(week_lines)
            db[row.ts_code] = pickle.dumps(week_lines)

        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

from datasource_tushare import datasource_ts as ds_ts
import pmas
from math import isnan
import dbm
import pickle
import os


if __name__ == '__main__':
    try:
        # last_day_line = util.get_last_day_line_close_price()
        db = dbm.open(os.getcwd() + '/dbms/month_line.dbm', 'c')
        ds = ds_ts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            month_lines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                month_lines = pickle.loads(data)

            #df2 = ds.get_monthline(row.ts_code)
            df2 = ds.get_month_line(row.ts_code, start_date='19800101')
            if df2 is None:
                continue
            for row2 in df2.itertuples():
                print(row2)
                if isnan(row2.close):
                    continue
                if row2.trade_date not in month_lines:
                    month_lines[row2.trade_date] = {}
                    month_lines[row2.trade_date]['raw'] = [row2.open, row2.high, row2.low, row2.close, row2.pre_close,
                                                           row2.vol, row2.amount]

            pmas.cal_pmas(month_lines)
            # del db[row.ts_code]
            db[row.ts_code] = pickle.dumps(month_lines)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

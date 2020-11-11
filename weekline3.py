from datasource_tushare import datasource_ts as dsts
from zhibiao_calculator import pma_calculator
from math import isnan
import dbm
import pickle
import os


if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/weekline.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            weeklines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                weeklines = pickle.loads(data)

            df2 = ds.get_weekline(row.ts_code)
            #df2 = ds.get_weekline(row.ts_code, start_date='19800101')
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                if isnan(row.close):
                    continue
                if row.trade_date not in weeklines:
                    weeklines[row.trade_date] = {}
                    weeklines[row.trade_date]['raw'] = [row.open, row.high, row.low, row.close, row.pre_close, row.vol, row.amount]

            pma_calculator.cal_pmas(weeklines)
            db[row.ts_code] = pickle.dumps(weeklines)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
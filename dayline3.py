from datasource_tushare import datasource_ts as dsts
from math import isnan
import dbm
import json


if __name__ == '__main__':
    try:
        db = dbm.open('dayline.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            daylines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                daylines = json.loads(data)

            df2 = ds.get_dayline(row.ts_code)
            #df2 = ds.get_dayline(row.ts_code, start_date='19800101')
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                if isnan(row.close):
                    continue
                if row.trade_date not in daylines:
                    daylines[row.trade_date] = [row.open, row.high, row.low, row.close, row.pre_close, row.vol, row.amount]
            #db.put(bytes(row.ts_code, encoding='utf8'), pickle.dumps(daylines))
            db[row.ts_code] = json.dumps(daylines)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
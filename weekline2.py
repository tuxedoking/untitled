from datasource_tushare import datasource_ts as dsts
from math import isnan
import rocksdb
import pickle


if __name__ == '__main__':
    try:
        db = rocksdb.DB("weekline.db", rocksdb.Options(create_if_missing=True))
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            # print(row) print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
            data = db.get(bytes(row.ts_code, encoding='utf8'))
            if data is not None:
                weeklines = pickle.loads(data)
            else:
                weeklines = {}
            df2 = ds.get_weekline(row.ts_code, '19800901')
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                if isnan(row.close):
                    continue
                if row.trade_date not in weeklines:
                    weeklines[row.trade_date] = [row.open, row.high, row.low, row.close, row.pre_close, row.vol, row.amount]
            db.put(bytes(row.ts_code, encoding='utf8'), pickle.dumps(weeklines))
    except Exception as err:
        print(err)
    finally:
        pass
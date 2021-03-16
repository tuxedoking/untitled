import pickle
from datasource_tushare import datasource_ts as ds_ts
import dbm
import os
import time


def get_hk_hold(trade_date):
    try:
        db = dbm.open(os.getcwd() + '/dbms/hk_hold.dbm', 'c')
        ds = ds_ts.Datasource()
        df = ds.get_hk_hold(trade_date=trade_date)
        for row in df.itertuples():
            if row.exchange != 'SH' and row.exchange != 'SZ':
                continue
            print(row)
            data = None
            hold = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                hold = pickle.loads(data)

            hold[row.trade_date] = {'vol': row.vol, 'ratio': row.ratio}
            print(hold)
            db[row.ts_code] = pickle.dumps(hold)

        db.close()
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    get_hk_hold(20210315)
    # ds = ds_ts.Datasource()
    # day_set = ds.get_trade_days()
    # day_list = sorted(day_set, reverse=True)[0:100]
    # for trade_date2 in day_list:
    #     get_hk_hold(trade_date2)
    #     time.sleep(30)


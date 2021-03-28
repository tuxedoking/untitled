import pickle
from datasource_tushare import datasource_ts as ds_ts
import dbm
import os
import time
import pandas as pd


def get_hk_hold(trade_date):
    try:
        db = dbm.open(os.getcwd() + '/dbms/hk_hold.dbm', 'c')
        ds = ds_ts.Datasource()
        df = ds.get_hk_hold(trade_date=trade_date)
        print(df)
        for index in df.index:
            if df.loc[index, 'exchange'] != 'SH' and df.loc[index, 'exchange'] != 'SZ':
                continue
            code = df.loc[index, 'ts_code']
            trade_date = df.loc[index, 'trade_date']
            vol = int(df.loc[index, 'vol'])
            ratio = df.loc[index, 'ratio']

            data = None
            hold = {}
            try:
                data = db[code]
            except KeyError:
                pass
            if data is not None:
                hold = pickle.loads(data)

            hold[trade_date] = {'vol': vol, 'ratio': ratio}
            print(hold)
            db[code] = pickle.dumps(hold)

    except Exception as err:
        print(err)
    finally:
        db.close()


if __name__ == '__main__':
    get_hk_hold(20210326)
    # ds = ds_ts.Datasource()
    # day_set = ds.get_trade_days()
    # day_list = sorted(day_set, reverse=True)[0:100]
    # for trade_date2 in day_list:
    #     get_hk_hold(trade_date2)
    #     time.sleep(30)


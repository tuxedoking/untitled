import dbm
import pickle
import os
import pandas as pd
from datasource_tushare import datasource_ts as ds_ts

if __name__ == '__main__':
    try:
        pd.set_option('display.max_columns', 1000)
        ds = ds_ts.Datasource()
        df_code_list = ds.get_code_list()
        db = dbm.open('E:/dbms/day_line.dbm')
        # db = dbm.open('E:/dbms/week_line.dbm', 'c')
        # db = dbm.open('E:/dbms/month_line.dbm', 'c')
        # print(db.get(';a;a'))
        for key in db.keys():
            data = db[key]
            df = pickle.loads(data)
            code = bytes.decode(key)
            # for date in sorted(lines, reverse=True):
            #     print(code, date, lines[date])
            #     break
            print(code)
            print(df[0:10])
            # db[code] = pickle.dumps(df.set_index('trade_date'))
        print('stock count = ', len(df_code_list))
    except Exception as err:
        print(err)
    finally:
        db.close()

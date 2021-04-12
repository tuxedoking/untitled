import dbm
import pickle
import os
from datasource_tushare import datasource_ts as ds_ts

if __name__ == '__main__':
    try:
        ds = ds_ts.Datasource()
        df_code_list = ds.get_code_list()
        # db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        for i, key in enumerate(db.keys(), 1):
            data = db[key]
            df = pickle.loads(data)
            code = bytes.decode(key)
            # for date in sorted(lines, reverse=True):
            #     print(code, date, lines[date])
            #     break
            print(i, code, df.iloc[0, 1])
        print('stock count = ', len(df_code_list))
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

from datasource_tushare import datasource_ts as ds_ts
from datasource_tushare import mysql_helper as mh
from math import isnan

if __name__ == '__main__':
    try:
        mysql = mh.Mysql_Helper()
        ds = ds_ts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            df2 = ds.get_day_line(row.ts_code)
            print(row.ts_code)
            if df2 is None:
                continue

            for row2 in df2.itertuples():
                print(row2)
                if isnan(row2.close):
                    continue
                sql = "replace into dayline2_qfq (obj,date,open,high,low,close,vol,amout,updatetime) values " \
                      "('%s','%s','%s','%s','%s','%s','%s','%s',now())" \
                      % (row.ts_code, row2.trade_date, row2.open, row2.high,
                         row2.low, row2.close, row2.vol, row2.amount)
                print(sql)
                mysql.runsql(sql)

    except Exception as err:
        print(err)
    finally:
        mysql.close()

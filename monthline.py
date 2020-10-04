from datasource_tushare import datasource_ts as dsts
from datasource_tushare import mysql_helper as mh
import math


if __name__ == '__main__':
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            # print(row) print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
            df2 = ds.get_monthline(row.ts_code)
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                #print(math.isnan(row.close))
                #if row.close.isnan():
                #    print(row)
                #    exit(0)
                if math.isnan(row.close):
                    continue
                sql = "replace into monthline (obj,date,open,high,low,close,preclose,vol,amount,updatetime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',now())"\
                    % (row.ts_code, row.trade_date, row.open, row.high, row.low, row.close, row.pre_close, row.vol, row.amount)
                print(sql)
                mysql.runsql(sql)
    except Exception as err:
        print(err)
    finally:
        mysql.close()
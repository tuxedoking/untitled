from datasource_tushare import datasource_ts as dsts
from datasource_tushare import mysql_helper as mh
from math import isnan


if __name__ == '__main__':
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            # print(row) print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
            df2 = ds.get_weekline(row.ts_code, '19800101')
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                if isnan(row.close):
                    continue
                sql = "replace into weekline2_qfq (obj,date,open,high,low,close,vol,amout,updatetime) values ('%s','%s','%s','%s','%s','%s','%s','%s',now())"\
                    % (row.ts_code, row.trade_date, row.open, row.high, row.low, row.close, row.vol, row.amount)
                print(sql)
                mysql.runsql(sql)
    except Exception as err:
        print(err)
    finally:
        mysql.close()
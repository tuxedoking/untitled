from datasource_tushare import datasource_ts as dsts
from datasource_tushare import mysql_helper as mh


if __name__ == '__main__':
    try:
        ds = dsts.Datasource()
        df = ds.get_code_list()
        mysql = mh.Mysql_Helper()
        for row in df.itertuples():
            #print(row) print(row.Index, row.ts_code, row.symbol, row.name, row.area, row.industry, row.list_date)
            sql = "replace into code (obj,name,updatetime) VALUES ('%s','%s',now())" % (row.ts_code, row.name)
            print(sql)
            mysql.runsql(sql)
    except Exception as err:
        print(err)
    finally:
        mysql.close()

#from datasource_tushare import datasource_ts as dsts
import datasource_tushare.datasource_ts as dsts
import json


'''
if __name__ == '__main__':
    try:
        ds = dsts.Datasource()
        df = ds.get_code_list()
        print(df.to_dict())
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
'''


if __name__ == '__main__':
    try:
        ds = dsts.Datasource()
        df = ds.get_code_list()
        d = {}
        for row in df.itertuples():
            d[row.symbol] = row.name
        str = json.dumps(d, ensure_ascii=False)
        print(str)
        e = json.loads(str)
        print(e)
        print(type(e))
    except Exception as err:
        print(err)

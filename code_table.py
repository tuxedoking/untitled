#from datasource_tushare import datasource_ts as dsts
import datasource_tushare.datasource_ts as dsts
import json
import dbm


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

def read_codetable():
    try:
        db = dbm.open('../codetable.dbm')
        d = {}
        for key in db.keys():
            d[bytes.decode(key)] = bytes.decode(db[key])
        return d
    except Exception as err:
        return None


def write_codetable():
    try:
        db = dbm.open('codetable.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            db[row.ts_code] = row.name
        db.close()
    except Exception as err:
        print(err)


if __name__ == '__main__':
   codetable = read_codetable()
   for key,value in codetable.items():
       print(key,value)

#from datasource_tushare import datasource_ts as dsts
import datasource_tushare.datasource_ts as dsts
import json
import dbm
import os
from datasource_tushare import mysql_helper as mh


def read_codetable():
    try:
        db = dbm.open(os.getcwd() + '/dbms/codetable.dbm')
        d = {}
        for key in db.keys():
            d[bytes.decode(key)] = bytes.decode(db[key])
        return d
    except Exception as err:
        return None


def write_codetable():
    try:
        db = dbm.open(os.getcwd() + '/dbms/codetable.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            db[row.ts_code] = row.name
        db.close()
    except Exception as err:
        print(err)


def write_codetable2db():
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            sql = "replace into code (obj,name,updatetime) values ('%s','%s',now())" \
                  % (row.ts_code, row.name)
            print(sql)
            mysql.runsql(sql)
    except Exception as err:
        print(err)
        mysql.close()


if __name__ == '__main__':
    write_codetable()
    write_codetable2db()

    codetable = read_codetable()
    for key,value in codetable.items():
        print(key,value)

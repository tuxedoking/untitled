import datasource_tushare.datasource_ts as dsts
import dbm
import os
import pandas as pd
from datasource_tushare import mysql_helper as mh


def read_codetable(filename):
    try:
        db = dbm.open(filename)
        jsonstr = db['codetable']
        df = pd.read_json(jsonstr)
        d = {}
        for index in df.index:
            d[df.loc[index, 'ts_code']] = df.loc[index, 'name']
        return d
    except Exception as err:
        return None


def write_codetable2dbm():
    try:
        db = dbm.open(os.getcwd() + '/dbms/codetable.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        df_str = df.to_json()
        db['codetable'] = df_str
    except Exception as err:
        print(err)


def write_codetable2db():
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for index in df.index:
            sql = "replace into code (obj,name,updatetime) values ('%s','%s',now())" % (df.loc[index, 'ts_code'], df.loc[index, 'name'])
            print(sql)
            mysql.runsql(sql)
    except Exception as err:
        print(err)
        mysql.close()


if __name__ == '__main__':
    write_codetable2dbm()
    write_codetable2db()
    # write_codetable_kzz()

    codetable = read_codetable(os.getcwd() + '/dbms/codetable.dbm')
    for key, value in codetable.items():
        print(key, value)

    # codetable_kzz = read_codetable_kzz()
    # for key, value in codetable_kzz.items():
    #    print(key, value)

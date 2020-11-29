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


def read_codetable_kzz():
    try:
        db = dbm.open(os.getcwd() + '/dbms/codetable_kzz.dbm')
        d = {}
        for key in db.keys():
            d[bytes.decode(key)] = bytes.decode(db[key])
        return d
    except Exception as err:
        return None


def write_codetable_kzz():
    try:
        db = dbm.open(os.getcwd() + '/dbms/codetable_kzz.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list_kzz()
        for row in df.itertuples():
            db[row.ts_code] = row.bond_short_name
        db.close()
    except Exception as err:
        print(err)


def write_codetable2dbm():
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
    write_codetable2dbm()
    write_codetable2db()
    write_codetable_kzz()

    codetable = read_codetable()
    for key, value in codetable.items():
        print(key, value)

    codetable_kzz = read_codetable_kzz()
    for key, value in codetable_kzz.items():
        print(key, value)

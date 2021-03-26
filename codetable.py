import datasource_tushare.datasource_ts as dsts
import dbm
import os
from datasource_tushare import mysql_helper as mh
import pickle
import datetime


def read_codetable(file_name):
    try:
        db = dbm.open(file_name)
        last_time = pickle.loads(db['time'])
        if (datetime.datetime.now() - last_time).seconds > 3:
            write_codetable2dbm(file_name)
        df_bytes = db['codetable']
        df = pickle.loads(df_bytes)
        d = {}
        for index in df.index:
            d[df.loc[index, 'ts_code']] = df.loc[index, 'name']
        return d
    except Exception as err:
        print(err)
        return None
    finally:
        db.close()


def write_codetable2dbm(file_name):
    try:
        db = dbm.open(file_name, 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        db['codetable'] = pickle.dumps(df)
        db['time'] = pickle.dumps(datetime.datetime.now())
    except Exception as err:
        print(err)
    finally:
        db.close()


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
    file_name = os.getcwd() + '/dbms/codetable.dbm'
    codetable = read_codetable(file_name)
    for key, value in codetable.items():
       print(key, value)


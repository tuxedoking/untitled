import datasource_tushare.datasource_ts as dsts
from datasource_tushare import mysql_helper as mh


def write_codetable2db():
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for index in df.index:
            sql = "replace into code (obj,name,updatetime) values ('%s','%s',now())" % (
            df.loc[index, 'ts_code'], df.loc[index, 'name'])
            print(sql)
            mysql.runsql(sql)
    except Exception as err:
        print(err)
        mysql.close()


if __name__ == '__main__':
    write_codetable2db()

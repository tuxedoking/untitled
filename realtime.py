from datasource_tushare import mysql_helper as mh
from datasource_tushare import datasource_ts as dsts
from datasource_tushare import change_code2tscode as cctc

def getlastdayline():
    mysql = mh.Mysql_Helper()
    cursor = mysql.connection.cursor()
    d = {}
    try:
        with mysql.connection.cursor() as cursor:
            # Create a new record
            sql = "select max(date),obj from dayline group by obj"
            cursor.execute(sql)
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                code = result[1][0:6]
                date = result[0]
                d[code] = date
                #print(date, code)
            return d
    except Exception as err:
        print(err)
    finally:
        mysql.close()


if __name__ == '__main__':
    #print(getlastdayline())
    try:
        mysql = mh.Mysql_Helper()
        ds = dsts.Datasource()
        df = ds.get_todayline()
        if df is None:
            print("get code list error")
        count = 0
        for row in df.itertuples():
            print(row)
            ts_code = cctc.change_code2tscode(row.code)
            if ts_code is None:
                print(ts_code)
                continue
            count += 1
            #sql = "replace into dayline (obj,date,open,high,low,close,preclose,vol,amount,updatetime) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s',now())" \
            #      % (ts_code, row.trade_date, row.open, row.high, row.low, row.close, row.pre_close, row.vol,
            #         row.amount)
            #print(sql)
            #mysql.runsql(sql)
        print(count)
    except Exception as err:
        print(err)
    finally:
        mysql.close()

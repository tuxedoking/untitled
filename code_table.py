#from datasource_tushare import datasource_ts as dsts
import datasource_tushare.datasource_ts as dsts
import json
import dbm


def read_codetable():
    try:
        db = dbm.open('E:/PycharmProjects/dbms/codetable.dbm')
        d = {}
        for key in db.keys():
            d[bytes.decode(key)] = bytes.decode(db[key])
        return d
    except Exception as err:
        return None


def write_codetable():
    try:
        db = dbm.open('E:/PycharmProjects/dbms/codetable.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            db[row.ts_code] = row.name
        db.close()
    except Exception as err:
        print(err)


if __name__ == '__main__':
    write_codetable()
    '''
   codetable = read_codetable()
   for key,value in codetable.items():
       print(key,value)
    '''
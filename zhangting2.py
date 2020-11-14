import dbm
import pickle
import sys
import codetable
import os

if __name__ == '__main__':
    startdate = 19800101
    enddate = 20500101
    code_table = codetable.read_codetable()
    for i in range(len(sys.argv)):
        if i == 1:
            startdate = int(sys.argv[1])
        if i == 2:
            enddate = int(sys.argv[2])

    try:
        db = dbm.open(os.getcwd() + '/dbms/dayline.dbm')
        for key in db.keys():
            data = db[key]
            daylines = pickle.loads(data)
            code = bytes.decode(key)
            for date in sorted(daylines):
                if int(date) >= startdate and int(date) <= enddate:
                    preclose = daylines[date]['raw'][4]
                    close = daylines[date]['raw'][0]
                    zhangfu = (close-preclose)/preclose
                    if zhangfu > 0.09:
                        print(code, code_table[code], date)
                    #print(code, date, daylines[date])
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
import dbm
import json
import sys


if __name__ == '__main__':
    print(sys.argv)
    startdate = 19800101
    enddate = 20500101
    for i in range(len(sys.argv)):
        if i == 1:
            startdate = int(sys.argv[1])
        if i == 2:
            enddate = int(sys.argv[2])

    try:
        db = dbm.open('../dayline.dbm')
        for key in db.keys():
            data = db[key]
            daylines = json.loads(data)
            code = bytes.decode(key)
            for date in sorted(daylines):
                if int(date) >= startdate and int(date) <= enddate:
                    preclose = daylines[date][4]
                    close = daylines[date][0]
                    zhangfu = (close-preclose)/preclose
                    if zhangfu > 0.09:
                        print(code, date)
                    #print(code, date, daylines[date])
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
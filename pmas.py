import dbm
import pickle
import os
import sys


def cal_pmas(lines):
    pmas = []
    for date in sorted(lines):
        close = lines[date]['raw'][3]
        pmas.append(close)
        if len(pmas) >= 5:
            lines[date]['pma5'] = sum(pmas[-5:])/5
        if len(pmas) >= 10:
            lines[date]['pma10'] = sum(pmas[-10:])/10
        if len(pmas) >= 20:
            lines[date]['pma20'] = sum(pmas[-20:])/20
        if len(pmas) >= 30:
            lines[date]['pma30'] = sum(pmas[-30:])/30
        if len(pmas) >= 60:
            lines[date]['pma60'] = sum(pmas[-60:])/60
        if len(pmas) >= 120:
            lines[date]['pma120'] = sum(pmas[-120:])/120
        if len(pmas) >= 250:
            lines[date]['pma250'] = sum(pmas[-250:])/250


def cal250up(lines):
    count = 0
    last = -1
    flag = False
    count2 = 0
    for date in sorted(lines, reverse=True):
        if 'pma250' not in lines[date]:
            break
        else:
            if last == -1:
                lastest = lines[date]['pma250']
                last = lastest
                continue
            else:
                pma250 = lines[date]['pma250']
                if pma250 <= last:
                    if flag = False:
                        last = pma250
                        count += 1
                else:
                    flag = True
                    count2 += 1
                    break
    if count == 0:
        return 0, 0.0
    return count, 100*(lastest - pma250)/pma250
    #return count


'''
if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/dayline.dbm')
        for key in db.keys():
            print(key)
            data = db[key]
            daylines = json.loads(data)
            cal_pmas(daylines)
            db[key] = json.dumps(daylines)
            #code = bytes.decode(key)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
'''
if __name__ == '__main__':
    try:
        print(os.getcwd())
        db = dbm.open(os.getcwd() + '/dbms/dayline.dbm')
        for key in db.keys():
            data = db[key]
            code = bytes.decode(key)
            #print(code)
            if code == '600549.SH':
                iii = 999
            daylines = pickle.loads(data)
            daycount,fd = cal250up(daylines)
            if daycount >= 30 and daycount < 200 and fd > 3:
                print(code, daycount, fd)
        db.close()
    except Exception as err:
        s = sys.exc_info()
        print(err, s[2].tb_lineno)
    finally:
        pass




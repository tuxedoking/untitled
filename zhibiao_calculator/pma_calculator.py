import dbm
import json


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


if __name__ == '__main__':
    try:
        db = dbm.open('../dayline.dbm', 'c')
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





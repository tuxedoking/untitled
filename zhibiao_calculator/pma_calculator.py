import dbm
import json


def cal_pma(pmas, count):
    pma = sum(pmas) / float(count)
    del pmas[0]
    return pma


def cal_pmas(lines):
    pma5s = []
    pma10s = []
    pma20s = []
    pma30s = []
    pma60s = []
    pma120s = []
    pma250s = []
    for date in sorted(lines):
        close = lines[date]['raw'][3]
        pma5s.append(close)
        pma10s.append(close)
        pma20s.append(close)
        pma30s.append(close)
        pma60s.append(close)
        pma120s.append(close)
        pma250s.append(close)

        if len(pma5s) == 5:
            lines[date]['pma5'] = cal_pma(pma5s, 5)
        if len(pma10s) == 10:
            lines[date]['pma10'] = cal_pma(pma10s, 10)
        if len(pma20s) == 20:
            lines[date]['pma20'] = cal_pma(pma20s, 20)
        if len(pma30s) == 30:
            lines[date]['pma30'] = cal_pma(pma30s, 30)
        if len(pma60s) == 60:
            lines[date]['pma60'] = cal_pma(pma60s, 60)
        if len(pma120s) == 120:
            lines[date]['pma120'] = cal_pma(pma120s, 120)
        if len(pma250s) == 250:
            lines[date]['pma250'] = cal_pma(pma250s, 250)


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





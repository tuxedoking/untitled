import dbm
import os
import pickle
from bolangs import cal_bo_lang_s


if __name__ == '__main__':
    try:
        db_month_line_bo_lang_s = dbm.open(os.getcwd() + '/dbms/month_line_bo_lang_s.dbm', 'c')
        db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        for key in db.keys():
            data = db[key]
            lines2 = pickle.loads(data)
            code = bytes.decode(key)

            # if code == '601677.SH':
            #    iii = 999

            bo_lang_s2 = cal_bo_lang_s(lines2)
            print(code, bo_lang_s2)
            del db_month_line_bo_lang_s[code]
            db_month_line_bo_lang_s[code] = pickle.dumps(bo_lang_s2)
        db.close()
        db_month_line_bo_lang_s.close()
    except Exception as err:
        print(err)
    finally:
        pass

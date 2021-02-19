import dbm
import pickle
import os

if __name__ == '__main__':
    try:
        # db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        for key in db.keys():
            data = db[key]
            lines = pickle.loads(data)
            code = bytes.decode(key)
            for date in sorted(lines, reverse=True):
                print(code, date)
                break
        db.close()

        db_bo_lang_s = dbm.open(os.getcwd() + '/dbms/bo_lang_s.dbm')
        for key in db_bo_lang_s.keys():
            data = db_bo_lang_s[key]
            bo_lang_s = pickle.loads(data)
            code = bytes.decode(key)
            print(code, bo_lang_s)
        db_bo_lang_s.close()
    except Exception as err:
        print(err)
    finally:
        pass

import dbm
import pickle
import os

if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/day_line_bo_lang_s.dbm')
        for key in db.keys():
            data = db[key]
            bo_lang_s = pickle.loads(data)
            code = bytes.decode(key)
            if code == '002588.SZ':
                print(code, bo_lang_s)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

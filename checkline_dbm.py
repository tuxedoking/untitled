import dbm
import pickle
import os

if __name__ == '__main__':
    try:
        db = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        # db = dbm.open(os.getcwd() + '/dbms/month_line.dbm')
        for key in db.keys():
            data = db[key]
            lines = pickle.loads(data)
            code = bytes.decode(key)
            for date in sorted(lines, reverse=True):
                print(code, date, lines[date])
                break
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

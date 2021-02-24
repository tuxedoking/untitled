import pickle
import codetable
import dbm
import os
import json


if __name__ == '__main__':
    try:
        # codes = {'002531.SZ', '300418.SZ'}
        code_table = codetable.read_codetable(os.getcwd() + '/dbms/codetable.dbm')
        db = dbm.open(os.getcwd() + '/dbms/hk_hold.dbm')
        with open(os.getcwd() + '/select_result/hk_hold.txt', 'w') as f:
            for key in db.keys():
                data = db[key]
                hold = pickle.loads(data)
                code = bytes.decode(key)
                # print(code)
                # print(json.dumps(hold))
                if code not in code_table:
                    continue
                f.write(code + ' ' + code_table[code] + '\n')
                for date in sorted(hold):
                    if hold[date]['ratio'] > 2:
                        f.write('\t' + date + json.dumps(hold[date]) + '\n')
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass

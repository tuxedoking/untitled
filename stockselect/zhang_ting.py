import dbm
import pickle
import sys
import codetable
import os
from util import is_zt
from util import get_start_date
from util import __end_date
from util import get_stock_name
import csv


def select():
    try:
        start_date = get_start_date()
        with open(os.getcwd() + '/../select_result/涨停.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['日期', '代码', '名称', '数量'])
            csv_writer.writerow(['80', '60', '80', '60'])
            csv_writer.writerow(['int', 'string', 'string', 'int'])

            db = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
            for key in db.keys():
                data = db[key]
                day_lines = pickle.loads(data)
                code = bytes.decode(key)
                count = 0
                for date in sorted(day_lines, reverse=True):
                    if int(date) > __end_date:
                        continue
                    elif start_date <= int(date) <= __end_date:
                        pre_close = day_lines[date]['raw'][4]
                        close = day_lines[date]['raw'][3]
                        b = is_zt(pre_close, close)
                        if b is True:
                            if count == 0:
                                to_date = date
                            count += 1
                        else:
                            if count > 0:
                                result_row = [to_date, code[0:6], get_stock_name(code), count]
                                csv_writer.writerow(result_row)
                                print(result_row)
                            count = 0
                    elif int(date) < start_date:
                        break
            db.close()
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    select()
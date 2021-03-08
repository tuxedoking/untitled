import dbm
import pickle
import codetable
import os
from util import get_stock_name
from util import get_start_date
from util import __end_date
import csv


MAX_DAY_COUNT = 50


def select():
    try:
        start_date = get_start_date()
        with open(os.getcwd() + '/../select_result/创新高.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['日期', '代码', '名称', '天数'])
            csv_writer.writerow(['80', '60', '80', '60'])
            csv_writer.writerow(['int', 'string', 'string', 'int'])

            db = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
            for key in db.keys():
                data = db[key]
                lines = pickle.loads(data)
                code = bytes.decode(key)
                count = 0
                for date in sorted(lines, reverse=True):
                    if int(date) > __end_date:
                        continue
                    elif start_date <= int(date) <= __end_date:
                        to_date = int(date)
                        to_close = lines[date]['raw'][3]
                        for date2 in sorted(lines, reverse=True):
                            if date2 >= date:
                                continue
                            else:
                                if lines[date2]['raw'][3] < to_close:
                                    count += 1
                                else:
                                    if count > MAX_DAY_COUNT:
                                        result_row = [to_date, code[0:6], get_stock_name(code), count]
                                        csv_writer.writerow(result_row)
                                        print(result_row)
                                    break
                        if count > MAX_DAY_COUNT:
                            break
                    elif int(date) < start_date:
                        break
            db.close()
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    select()

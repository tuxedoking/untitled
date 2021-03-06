import dbm
import pickle
import codetable
import os
from util import get_start_date
from util import __end_date
from util import get_stock_name
from util import get_zhang_fu
import csv


def select():
    try:
        start_date = get_start_date()
        with open(os.getcwd() + '/../select_result/日线多头排列.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['日期', '代码', '名称', '天数', '幅度'])
            csv_writer.writerow(['80', '60', '80', '60', '60'])
            csv_writer.writerow(['int', 'string', 'string', 'int', 'double'])

            db = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
            for key in db.keys():
                data = db[key]
                lines = pickle.loads(data)
                code = bytes.decode(key)
                # if code == '003001.SZ':
                #    sss = 999
                count = 0
                for date in sorted(lines, reverse=True):
                    # if date == '20201120':
                    #    sss = 999
                    if int(date) > __end_date:
                        continue
                    elif start_date <= int(date) <= __end_date:
                        if 'pma5' not in lines[date] or 'pma10' not in lines[date] or 'pma20' not in lines[date] or 'pma30' not in lines[date]:
                            break
                        pma5 = lines[date]['pma5']
                        pma10 = lines[date]['pma10']
                        pma20 = lines[date]['pma20']
                        pma30 = lines[date]['pma30']
                        if pma5 > pma10 > pma20 > pma30:
                            if count == 0:
                                zhang_fu = get_zhang_fu(pma30, pma5)
                                if zhang_fu > 5:    # ma5和ma30涨幅>5
                                    to_date = date
                                    count += 1
                                else:
                                    continue
                            else:
                                count += 1
                        else:
                            if count >= 5:  # 连续走5天以上的多头排列
                                result_row = [to_date, code[0:6], get_stock_name(code), count, zhang_fu]
                                csv_writer.writerow(result_row)
                                print(result_row)
                            count = 0
                    elif int(date) < start_date:
                        break
            db.close()
    except Exception as err:
        print(code)
        print(err)
    finally:
        pass


if __name__ == '__main__':
    select()

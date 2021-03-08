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
        with open(os.getcwd() + '/../select_result/日线上涨回调(5).csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['回调低点日期', '代码', '名称', '上涨幅度', '回调幅度'])
            csv_writer.writerow(['100', '60', '80', '60', '60'])
            csv_writer.writerow(['int', 'string', 'string', 'double', 'double'])

            db_day_line = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
            db_day_line_bo_lang_s = dbm.open(os.getcwd() + '/../dbms/day_line_bo_lang_s.dbm')

            for key in db_day_line_bo_lang_s.keys():
                data = db_day_line_bo_lang_s[key]
                bo_lang_s = pickle.loads(data)
                code = bytes.decode(key)
                flag = False
                to_date2 = ''
                for bo_lang in reversed(bo_lang_s):
                    # print(bo_lang)
                    from_date = bo_lang['from']
                    to_date = bo_lang['to']
                    if int(to_date) < start_date:
                        break
                    day_lines = pickle.loads(db_day_line[key])
                    from_close = day_lines[from_date]['raw'][3]
                    to_close = day_lines[to_date]['raw'][3]
                    if bo_lang['qu_shi'] == '下':
                        down_fu_du = get_zhang_fu(from_close, to_close)
                        if down_fu_du < -10:
                            to_date2 = to_date
                            flag = True
                        else:
                            flag = False
                    else:
                        if flag:
                            up_fu_du = get_zhang_fu(from_close, to_close)
                            if get_zhang_fu(from_close, to_close) > 20:
                                result_row = [to_date2, code[0:6], get_stock_name(code), up_fu_du, down_fu_du]
                                csv_writer.writerow(result_row)
                                print(result_row)
                            flag = False
                            #break

            db_day_line_bo_lang_s.close()
            db_day_line.close()

            '''
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
            '''
    except Exception as err:
        print(err)
    finally:
        pass


if __name__ == '__main__':
    select()

import pickle
from stockselect import util
from stockselect.selector import selector


class yue_xian_lian_yang(selector):
    def select(self, **kwargs):
        try:
            if 'start_date' not in kwargs:
                return None
            start_date = kwargs['start_date']
            items = []
            cache_key = __file__ + start_date

            if cache_key in selector.result_cache:
                return selector.result_cache[cache_key]

            for key in selector.db_month_lines.keys():
                data = selector.db_month_lines[key]
                df_lines = pickle.loads(data)
                code = bytes.decode(key)
                to_date = ''
                flag_count = 0

                for date in df_lines.index:
                    if date < start_date:
                        break
                    close = df_lines.loc[date, 'close']
                    pre_close = df_lines.loc[date, 'pre_close']
                    open = df_lines.loc[date, 'open']
                    if close > pre_close and close > open:
                        flag_count += 1
                        if flag_count == 1:
                            to_date = date
                    else:
                        if flag_count >= 3:
                            zhang_fu = util.get_zhang_fu(df_lines.loc[date, 'close'], df_lines.loc[to_date, 'close'])
                            if zhang_fu >= 10:
                                item = (to_date, code, util.get_stock_name(code), zhang_fu, flag_count)
                                items.append(item)
                                print(item)
                        flag_count = 0
            selector.result_cache[cache_key] = items
            return items
        except Exception as err:
            print(err)
            return None


if __name__ == '__main__':
    selector.init_dbs()
    a = yue_xian_lian_yang()
    a.select(start_date='20200101')

# import dbm
# import pickle
# import codetable
# import os
# from util import get_start_date_month_line
# from util import __end_date
# from util import get_zhang_fu
# from util import get_stock_name
# import csv
#
#
# def select():
#     try:
#         start_date = get_start_date_month_line()
#         with open(os.getcwd() + '/../select_result/月线连阳.csv', 'w', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             csv_writer.writerow(['日期', '代码', '名称', '涨幅', '数量'])
#             csv_writer.writerow(['80', '60', '80', '60', '40'])
#             csv_writer.writerow(['int', 'string', 'string', 'double', 'int'])
#
#             db = dbm.open(os.getcwd() + '/../dbms/month_line.dbm')
#             for key in db.keys():
#                 data = db[key]
#                 lines = pickle.loads(data)
#                 code = bytes.decode(key)
#                 flag_count = 0
#                 for date in sorted(lines, reverse=True):
#                     if int(date) > __end_date:
#                         continue
#                     elif start_date <= int(date) <= __end_date:
#                         line = lines[date]['raw']
#                         close = line[3]
#                         pre_close = line[4]
#                         open2 = line[0]
#                         if close > pre_close and close > open2:
#                             flag_count += 1
#                             if flag_count == 1:
#                                 to_date = date
#                         else:
#                             if flag_count >= 3:
#                                 zhang_fu = get_zhang_fu(lines[date]['raw'][3], lines[to_date]['raw'][3])
#                                 if zhang_fu >= 10:
#                                     result_row = [to_date, code[0:6], get_stock_name(code), zhang_fu, flag_count]
#                                     csv_writer.writerow(result_row)
#                                     print(result_row)
#                                 flag_count = 0
#                             else:
#                                 flag_count = 0
#                     elif int(date) < start_date:
#                         break
#             db.close()
#     except Exception as err:
#         print(err)
#     finally:
#         pass
#
#
# if __name__ == '__main__':
#     select()

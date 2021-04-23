import pickle
from stockselect import util
from stockselect.selector import selector


class yue_xian_duo_tou_pai_lie(selector):
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
                count = 0
                to_date = ''
                zhang_fu = 0

                for date in df_lines.index:
                    if date < start_date:
                        break
                    pma5 = df_lines.loc[date, 'pma5']
                    pma10 = df_lines.loc[date, 'pma10']
                    pma20 = df_lines.loc[date, 'pma20']
                    pma30 = df_lines.loc[date, 'pma30']
                    if pma5 > pma10 > pma20 > pma30:
                        if count == 0:
                            zhang_fu = util.get_zhang_fu(pma30, pma5)
                            if zhang_fu > 3:  # ma5和ma30涨幅>5
                                to_date = date
                                count += 1
                            else:
                                continue
                        else:
                            count += 1
                    else:
                        if count >= 5:  # 连续走5天以上的多头排列
                            item = (to_date, code, util.get_stock_name(code), count, zhang_fu)
                            items.append(item)
                            print(item)
                        count = 0
            selector.result_cache[cache_key] = items
            return items
        except Exception as err:
            print(err)
            return None


if __name__ == '__main__':
    selector.init_dbs()
    a = yue_xian_duo_tou_pai_lie()
    a.select(start_date='20210101')



# import dbm
# import pickle
# import codetable
# import os
# import util
# from util import get_start_date_month_line
# from util import __end_date
# import csv
#
#
# def select():
#     try:
#         start_date = get_start_date_month_line()
#         with open(os.getcwd() + '/../select_result/月线多头排列.csv', 'w', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             csv_writer.writerow(['日期', '代码', '名称', '天数', '幅度'])
#             csv_writer.writerow(['80', '60', '80', '60', '60'])
#             csv_writer.writerow(['int', 'string', 'string', 'int', 'double'])
#
#             db = dbm.open(os.getcwd() + '/../dbms/month_line.dbm')
#             for key in db.keys():
#                 data = db[key]
#                 lines = pickle.loads(data)
#                 code = bytes.decode(key)
#                 count = 0
#                 for date in sorted(lines, reverse=True):
#                     if int(date) > __end_date:
#                         continue
#                     elif start_date <= int(date) <= __end_date:
#                         if 'pma5' not in lines[date] or 'pma10' not in lines[date] or 'pma20' not in lines[date] or 'pma30' not in lines[date]:
#                             break
#                         pma5 = lines[date]['pma5']
#                         pma10 = lines[date]['pma10']
#                         pma20 = lines[date]['pma20']
#                         pma30 = lines[date]['pma30']
#                         if pma5 > pma10 > pma20 > pma30:
#                             if count == 0:
#                                 zhang_fu = util.get_zhang_fu(pma30, pma5)
#                                 if zhang_fu > 3:    # ma5和ma30涨幅>5
#                                     to_date = date
#                                     count += 1
#                                 else:
#                                     continue
#                             else:
#                                 count += 1
#                         else:
#                             if count >= 3:  # 连续走3天以上的多头排列
#                                 result_row = [to_date, code[0:6], util.get_stock_name(code), count, zhang_fu]
#                                 csv_writer.writerow(result_row)
#                                 print(result_row)
#                             count = 0
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

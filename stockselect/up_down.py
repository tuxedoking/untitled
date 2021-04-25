import pickle
from stockselect import util
from stockselect.selector import selector


class up_down(selector):
    def select(self, **kwargs):
        try:
            if 'start_date' not in kwargs:
                return None
            start_date = kwargs['start_date']
            items = []
            cache_key = __file__ + start_date

            if cache_key in selector.result_cache:
                return selector.result_cache[cache_key]

            for key in selector.db_day_line_bo_lang_s.keys():
                data = selector.db_day_line_bo_lang_s[key]
                bo_lang_s = pickle.loads(data)
                code = bytes.decode(key)
                flag = False
                to_date2 = ''
                for bo_lang in reversed(bo_lang_s):
                    to_date = bo_lang['to']
                    if to_date < start_date:
                        break
                    from_close = bo_lang['from_value']
                    to_close = bo_lang['to_value']
                    if bo_lang['qu_shi'] == '下':
                        down_fu_du = util.get_zhang_fu(from_close, to_close)
                        if down_fu_du < -10:
                            to_date2 = to_date
                            flag = True
                        else:
                            flag = False
                    else:
                        if flag:
                            up_fu_du = util.get_zhang_fu(from_close, to_close)
                            if up_fu_du > 20:
                                item = [to_date2, code, util.get_stock_name(code), up_fu_du, down_fu_du]
                                items.append(item)
                                print(item)
                        flag = False

            selector.result_cache[cache_key] = items
            return items
        except Exception as err:
            print(err)
            return None


if __name__ == '__main__':
    selector.init_dbs()
    a = up_down()
    a.select(start_date='20210101')
    selector.close_dbs()

# def select():
#     try:
#         start_date = get_start_date()
#         with open(os.getcwd() + '/../select_result/日线上涨回调(5).csv', 'w', newline='') as csv_file:
#             csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#             csv_writer.writerow(['回调低点日期', '代码', '名称', '上涨幅度', '回调幅度'])
#             csv_writer.writerow(['100', '60', '80', '60', '60'])
#             csv_writer.writerow(['int', 'string', 'string', 'double', 'double'])
#
#             db_day_line = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
#             db_day_line_bo_lang_s = dbm.open(os.getcwd() + '/../dbms/day_line_bo_lang_s.dbm')
#
#             for key in db_day_line_bo_lang_s.keys():
#                 data = db_day_line_bo_lang_s[key]
#                 bo_lang_s = pickle.loads(data)
#                 code = bytes.decode(key)
#                 flag = False
#                 to_date2 = ''
#                 for bo_lang in reversed(bo_lang_s):
#                     # print(bo_lang)
#                     from_date = bo_lang['from']
#                     to_date = bo_lang['to']
#                     if int(to_date) < start_date:
#                         break
#                     day_lines = pickle.loads(db_day_line[key])
#                     from_close = day_lines[from_date]['raw'][3]
#                     to_close = day_lines[to_date]['raw'][3]
#                     if bo_lang['qu_shi'] == '下':
#                         down_fu_du = get_zhang_fu(from_close, to_close)
#                         if down_fu_du < -10:
#                             to_date2 = to_date
#                             flag = True
#                         else:
#                             flag = False
#                     else:
#                         if flag:
#                             up_fu_du = get_zhang_fu(from_close, to_close)
#                             if get_zhang_fu(from_close, to_close) > 20:
#                                 result_row = [to_date2, code[0:6], get_stock_name(code), up_fu_du, down_fu_du]
#                                 csv_writer.writerow(result_row)
#                                 print(result_row)
#                             flag = False
#                             #break
#
#             db_day_line_bo_lang_s.close()
#             db_day_line.close()
#
#     except Exception as err:
#         print(err)
#     finally:
#         pass
#
#
# if __name__ == '__main__':
#     select()

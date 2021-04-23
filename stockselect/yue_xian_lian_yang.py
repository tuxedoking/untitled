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

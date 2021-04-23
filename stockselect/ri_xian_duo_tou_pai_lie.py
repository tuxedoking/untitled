import pickle
from stockselect import util
from stockselect.selector import selector


class ri_xian_duo_tou_pai_lie(selector):
    def select(self, **kwargs):
        try:
            if 'start_date' not in kwargs:
                return None
            start_date = kwargs['start_date']
            items = []
            cache_key = __file__ + start_date

            if cache_key in selector.result_cache:
                return selector.result_cache[cache_key]

            for key in selector.db_day_lines.keys():
                data = selector.db_day_lines[key]
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
                            if zhang_fu > 5:  # ma5和ma30涨幅>5
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
    a = ri_xian_duo_tou_pai_lie()
    a.select(start_date='20210101')


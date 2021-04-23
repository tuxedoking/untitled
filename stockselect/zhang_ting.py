import pickle
from stockselect import util
from stockselect.selector import selector


class zhang_ting(selector):
    def __init__(self):
        super().__init__()

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
                # df_lines = df_lines[df_lines.index >= start_date][['pre_close', 'close']]

                for date in df_lines.index:
                    if date < start_date:
                        break
                    b = util.is_zt(df_lines.loc[date, 'pre_close'], df_lines.loc[date, 'close'])
                    if b is True:
                        # item = (df_lines.loc(index, 'trade_date'), code, get_stock_name(code), count)
                        if count == 0:
                            to_date = date
                        count += 1
                    else:
                        if count > 0:
                            item = (to_date, code, util.get_stock_name(code), count)
                            items.append(item)
                            print(item)
                        count = 0
            selector.result_cache[cache_key] = items
            return items
        except Exception as err:
            print(err)
            return None


if __name__ == '__main__':
    a = zhang_ting()
    a.select(start_date='20210101')

import pickle
from util import is_zt
from util import get_stock_name
from stockselect.selector import selector


class zhang_ting(selector):
    def __init__(self):
        super().__init__()

    def select(self, **kwargs):
        try:
            if 'start_date' not in kwargs:
                return None
            if 'max_day_count' not in kwargs:
                max_day_count = 50
            else:
                max_day_count = kwargs['max_day_count']
            start_date = kwargs['start_date']
            items = []
            cache_key = __file__ + start_date + str(max_day_count)

            if cache_key in selector.result_cache:
                return selector.result_cache[cache_key]

            for key in self.db_day_lines.keys():
                data = self.db_day_lines[key]
                df_lines = pickle.loads(data)
                code = bytes.decode(key)
                count = 0
                to_date = ''
                for index in df_lines.index:
                    pre_close = df_lines.loc(index, 'pre_close')
                    close = df_lines.loc(index, 'close')
                    b = is_zt(pre_close, close)
                    if b is True:
                        # item = (df_lines.loc(index, 'trade_date'), code, get_stock_name(code), count)
                        if count == 0:
                            to_date = df_lines.loc(index, 'trade_date')
                        count += 1
                    else:
                        if count > 0:
                            item = (to_date, code, get_stock_name(code), count)
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

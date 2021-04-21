import os
import dbm


class selector(object):
    db_day_lines = dbm.open(os.getcwd() + '/../dbms/day_line.dbm')
    db_week_lines = dbm.open(os.getcwd() + '/../dbms/week_line.dbm')
    db_month_lines = dbm.open(os.getcwd() + '/../dbms/week_line.dbm')
    result_cache = {}

    @classmethod
    def select(cls, ):
        cls.result_cache['bbb'] = 999


if __name__ == '__main__':
    print(selector.result_cache)
    selector.result_cache['aaa'] = 666
    print(selector.result_cache)
    selector.hello()
    print(selector.result_cache)

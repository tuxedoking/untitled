import os
import dbm


class selector(object):
    result_cache = None
    db_day_lines = None
    db_week_lines = None
    db_month_lines = None

    @staticmethod
    def init_dbs():
        if selector.result_cache is not None:
            return
        selector.result_cache = {}
        selector.db_day_lines = dbm.open('E:/dbms/day_line.dbm')
        selector.db_week_lines = dbm.open('E:/dbms/week_line.dbm')
        selector.db_month_lines = dbm.open('E:/dbms/month_line.dbm')

    @staticmethod
    def close_dbs():
        selector.db_day_lines.close()
        selector.db_week_lines.close()
        selector.db_month_lines.close()

    def select(self, **kwargs):
        raise NotImplementedError


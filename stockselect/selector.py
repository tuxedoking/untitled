import os
import dbm


class selector(object):
    result_cache = {}
    db_day_lines = None
    db_week_lines = None
    db_month_lines = None

    @staticmethod
    def init_dbs():
        selector.result_cache = {}
        selector.db_day_lines = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        selector.db_week_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        selector.db_month_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')

    @staticmethod
    def close_dbs():
        selector.db_day_lines.close()
        selector.db_week_lines.close()
        selector.db_month_lines.close()

    def __init__(self):
        super().__init__()
        # self.db_day_lines = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        # self.db_week_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        # self.db_month_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')

    # def __del__(self):
    #     self.db_day_lines.close()
    #     self.db_week_lines.close()
    #     self.db_month_lines.close()

    def select(self, **kwargs):
        raise NotImplementedError


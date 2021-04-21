import os
import dbm


class selector(object):
    result_cache = {}

    def __init__(self):
        super().__init__()
        self.db_day_lines = dbm.open(os.getcwd() + '/dbms/day_line.dbm')
        self.db_week_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        self.db_month_lines = dbm.open(os.getcwd() + '/dbms/week_line.dbm')
        # self.result_cache = {}

    def __del__(self):
        self.db_day_lines.close()
        self.db_week_lines.close()
        self.db_month_lines.close()

    def select(self, **kwargs):
        raise NotImplementedError


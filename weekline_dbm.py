from datasource_tushare.datasource_ts import Datasource
import os
import pandas as pd
from stockselect import util


if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    file_name = os.getcwd() + '/dbms/week_line.dbm'
    util.put_lines_from_net_to_dbm(file_name, Datasource.get_week_line)

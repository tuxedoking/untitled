from datasource_tushare.datasource_ts import Datasource
import os
import pandas as pd
from stockselect import util
from lines_operator import lines_operator


if __name__ == '__main__':
    pd.set_option('display.max_columns', 1000)
    file_name = 'E:/dbms/month_line.dbm'
    op = lines_operator()
    op.put_lines_from_net_to_dbm(file_name, Datasource.get_month_line, 0.5)

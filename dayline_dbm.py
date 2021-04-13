import numpy as np

from datasource_tushare.datasource_ts import Datasource
import pmas
from math import isnan
import dbm
import pickle
import os
import sys
import time
import pandas as pd
from stockselect import util


if __name__ == '__main__':
    file_name = os.getcwd() + '/dbms/day_line.dbm'
    util.get_lines_to_dbm(file_name, Datasource.get_day_line)

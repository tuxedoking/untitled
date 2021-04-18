import dbm
import pickle
import time
import numpy as np
import pandas as pd
from datasource_tushare.datasource_ts import Datasource


class lines_operator:
    def __init__(self):
        self.last_t = 0
        self.periods = (5, 10, 20, 30, 60, 120, 250)

    def cal_pma_s_in_data_frame(self, df_lines):
        t = time.time()
        l4df = []
        close_array = np.array(df_lines['close'])
        for i, close in enumerate(close_array):
            d = {}
            for period in self.periods:
                if i + period > len(df_lines):
                    d[f'pma{period}'] = np.nan
                else:
                    a = close_array[i:i + period]
                    d[f'pma{period}'] = np.sum(a) / len(a)
            l4df.append(d)
        print('cal pma s', time.time() - t)
        return pd.concat([df_lines, pd.DataFrame(l4df, index=df_lines.index)], axis=1)

    def get_lines_from_net(self, ts_code, start_date, get_lines_from_net_fun_name, interval=0):
        if interval > 0:
            interval_last = time.time() - self.last_t
            # print('interval_last', interval_last, interval)
            if interval_last < interval:
                time.sleep(interval - interval_last)
                print('sleep ', interval - interval_last)
            self.last_t = time.time()

        df_from_net = get_lines_from_net_fun_name(ts_code, start_date=start_date)
        if df_from_net is None or len(df_from_net) == 0:
            return None
        return df_from_net.dropna(subset=['close']).set_index('trade_date')

    def put_lines_from_net_to_dbm(self, file_name, get_lines_from_net_fun_name, interval=0, before_day=20):
        try:
            db = dbm.open(file_name, 'c')
            ds = Datasource()
            df = ds.get_code_list()

            start_date_before_n = ds.get_last_n_trade_days(before_day)

            last_t = 0
            for index in df.index:
                ts_code = df.loc[index, 'ts_code']
                print(ts_code)

                data = db.get(ts_code)
                if data is None:
                    print('dbm里没有')
                    df_from_net = self.get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name, interval)
                    if df_from_net is None:
                        continue
                    # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                    # if df_from_net is None or len(df_from_net) == 0:
                    #     continue
                    # df_from_net = df_from_net.dropna(subset=['close'])
                    df_result = self.cal_pma_s_in_data_frame(df_from_net)
                    print(df_result)
                    db[ts_code] = pickle.dumps(df_result)
                    print(pickle.loads(db[ts_code]))
                else:
                    df_dbm = pickle.loads(data)

                    df_from_net = self.get_lines_from_net(ts_code, start_date_before_n, get_lines_from_net_fun_name,
                                                          interval)
                    if df_from_net is None:
                        continue
                    # df_from_net = get_lines_from_net_fun_name(ts_code, start_date=start_date_before_100)
                    # if df_from_net is None or len(df_from_net) == 0:
                    #     continue
                    # df_from_net = df_from_net.dropna(subset=['close'])

                    # trade_date1 = df_from_net.loc[df_from_net.index[df_from_net.shape[0] - 1], 'trade_date']
                    # trade_date2 = df_dbm.loc[0, 'trade_date']
                    trade_date1 = df_from_net.index[-1]
                    trade_date2 = df_dbm.index[0]
                    print('last date in net dataframe = ', trade_date1)
                    print('first date in dbm dataframe = ', trade_date2)
                    if trade_date1 > trade_date2:
                        df_from_net = self.get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name,
                                                              interval)
                        if df_from_net is None:
                            continue
                        # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                        # if df_from_net is None or len(df_from_net) == 0:
                        #     continue
                        # df_from_net = df_from_net.dropna(subset=['close'])
                        df_result = self.cal_pma_s_in_data_frame(df_from_net)
                        print(df_result)
                        db[ts_code] = pickle.dumps(df_result)
                    else:
                        db_merge = self.merge_lines(df_from_net, df_dbm)
                        # db_merge = merge_lines(df_from_net, df_dbm.drop([0, 1]))
                        if db_merge is None:
                            print('除权啦')
                            df_from_net = self.get_lines_from_net(ts_code, '19800101', get_lines_from_net_fun_name,
                                                                  interval)
                            if df_from_net is None:
                                continue
                            # df_from_net = get_lines_from_net_fun_name(ts_code, start_date='19800101')
                            # if df_from_net is None or len(df_from_net) == 0:
                            #     continue
                            # df_from_net = df_from_net.dropna(subset=['close'])
                            df_result = self.cal_pma_s_in_data_frame(df_from_net)
                            print(df_result)
                            db[ts_code] = pickle.dumps(df_result)
                        elif db_merge is df_dbm:
                            print('dbm里是全的')
                            pass
                        else:
                            print(db_merge)
                            db[ts_code] = pickle.dumps(db_merge)
        except Exception as err:
            print(err)
        finally:
            db.close()

    def merge_lines(self, df_net, df_dbm):
        i = 0
        for i, index in enumerate(df_net.index):
            if index == df_dbm.index[0]:
                if df_net.loc[index, 'open'] == df_dbm.loc[df_dbm.index[0], 'open'] \
                        and df_net.loc[index, 'high'] == df_dbm.loc[df_dbm.index[0], 'high'] \
                        and df_net.loc[index, 'low'] == df_dbm.loc[df_dbm.index[0], 'low'] \
                        and df_net.loc[index, 'close'] == df_dbm.loc[df_dbm.index[0], 'close']:
                    break
                else:
                    return None
            # if df_net.loc[index, 'trade_date'] == df_dbm.loc[df_dbm.index[0], 'trade_date']:
            #     if df_net.loc[index, 'open'] == df_dbm.loc[df_dbm.index[0], 'open'] \
            #             and df_net.loc[index, 'high'] == df_dbm.loc[df_dbm.index[0], 'high'] \
            #             and df_net.loc[index, 'low'] == df_dbm.loc[df_dbm.index[0], 'low'] \
            #             and df_net.loc[index, 'close'] == df_dbm.loc[df_dbm.index[0], 'close']:
            #         break
            #     else:
            #         return None
        if i == 0:
            return df_dbm

        print(f'新增{index}条记录')
        df_up = df_net.iloc[0:i]
        close_array = np.append(np.array(df_up['close']), np.array(df_dbm['close']))

        l4df = []
        for i, index in enumerate(df_up.index):
            d = {}
            for period in self.periods:
                if i + period > len(close_array):
                    d[f'pma{period}'] = np.nan
                else:
                    a = close_array[i:i + period]
                    d[f'pma{period}'] = np.sum(a) / len(a)
            l4df.append(d)

        df_up2 = pd.concat([df_up, pd.DataFrame(l4df, index=df_up.index)], axis=1)
        print(df_up2)
        return pd.concat([df_up2, df_dbm], axis=0)
        # return pd.concat([df_up2, df_dbm], axis=0).reset_index(drop=True)

from datasource_tushare import datasource_ts as dsts
from zhibiao_calculator import pma_calculator
from math import isnan
import dbm
import pickle


if __name__ == '__main__':
    try:
        db = dbm.open('monthline.dbm', 'c')
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for row in df.itertuples():
            data = None
            monthlines = {}
            try:
                data = db[row.ts_code]
            except KeyError:
                pass
            if data is not None:
                monthlines = pickle.loads(data)

            #df2 = ds.get_monthline(row.ts_code)
            df2 = ds.get_monthline(row.ts_code, start_date='19800101')
            if df2 is None:
                continue
            for row in df2.itertuples():
                print(row)
                if isnan(row.close):
                    continue
                if row.trade_date not in monthlines:
                    monthlines[row.trade_date] = {}
                    monthlines[row.trade_date]['raw'] = [row.open, row.high, row.low, row.close, row.pre_close, row.vol, row.amount]

            pma_calculator.cal_pmas(monthlines)
            db[row.ts_code] = pickle.dumps(monthlines)
        db.close()
    except Exception as err:
        print(err)
    finally:
        pass
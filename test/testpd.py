import datasource_tushare.datasource_ts as dsts
import pandas as pd


if __name__ == '__main__':
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 1000)
    try:
        ds = dsts.Datasource()
        df = ds.get_code_list()
        print(df.index)
        print(df.columns)
        print(df[df['area'].isin(['深圳', '上海'])])
        #print(df.loc[0:2, ['ts_code', 'symbol', 'name']])
        #print(df.iloc[1:3])
        #print(df['symbol'])
    except Exception as err:
        print(err)

import datasource_tushare.datasource_ts as dsts
import pandas as pd
import json


if __name__ == '__main__':
    pd.set_option('display.max_rows', 5000)
    pd.set_option('display.max_columns', 1000)
    try:
        ds = dsts.Datasource()
        df = ds.get_code_list()
        for index in df.index:
            print(df.loc[index, 'ts_code'], df.loc[index, 'name'])
        # jsonstr = df.to_json()
        # print(jsonstr)
        #
        # df2 = pd.read_json(jsonstr)
        # print(df2)
        #strdf = str(df)
        #print(strdf)
        #print(df)
        #print(df.index)
        #print(df.columns)
        #print(df[df['area'].isin(['深圳', '上海'])])
        #print(df.to_json())
        #df.to_csv
        #print(df.loc[0:2, ['ts_code', 'symbol', 'name']])
        #print(df.iloc[1:3])
        #print(df['symbol'])
    except Exception as err:
        print(err)

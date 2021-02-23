from datasource_tushare import datasource_ts as ds_ts


if __name__ == '__main__':
    ds = ds_ts.Datasource()
    df = ds.get_hk_hold('20210222')
    for row in df.itertuples():
        # print(row.ts_code)
        if row.ts_code == '002531.SZ' or row.ts_code == '300418.SZ':
            print(row)

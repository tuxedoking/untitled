import http.client
import time


def getsinahq(codes):
    try:
        strcode = ''
        for code in codes:
            strcode += code + ','
        conn = http.client.HTTPSConnection('hq.sinajs.cn', timeout=5)
        conn.request(method='GET', url='/?list=' + strcode)
        res = conn.getresponse()
        str = res.read().decode('gb18030')
        hqs = str.split(';\n')
        hqlist = []
        for hq in hqs:
            l1 = hq.split('=')
            if len(l1) < 2:
                break
            code = l1[0][-6:]
            l2 = l1[1].split(',')
            d = {}
            d['code'] = code
            d['name'] = l2[0]
            d['open'] = float(l2[1])
            d['last'] = float(l2[2])
            d['close'] = float(l2[3])
            d['high'] = float(l2[4])
            d['low'] = float(l2[5])
            hqlist.append(d)
        return hqlist
    except Exception as err:
        print(err)
    finally:
        conn.close()
    return None


'''
if __name__ == '__main__':
    print(getsinahq(['sh600549','sh000001']))
'''

if __name__ == '__main__':
    codes = ['sh000001', 'sh600549', 'sh601168', 'sh601360']
    while True:
        hqlist = getsinahq(codes)
        if hqlist is None:
            continue
        for hq in hqlist:
            zf = str(round(100 * (hq['close'] - hq['last']) / hq['last'], 2))
            if hq['close'] >= hq['last']:
                print('\033[31m' + hq['name'][1:2] + str(round(hq['close'], 2)) + '\033[0m')
                print('\033[31m' + '  ' + zf + '\033[0m')
            else:
                print('\033[40m' + hq['name'][1:2] + str(round(hq['close'], 2)) + '\033[0m')
                print('\033[40m' + '  ' + zf + '\033[0m')
        time.sleep(3)

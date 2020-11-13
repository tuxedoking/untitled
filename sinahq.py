import http.client
import time


def getsinahq(code):
    try:
        conn = http.client.HTTPSConnection('hq.sinajs.cn', timeout=5)
        conn.request(method='GET', url='/?list=' + code)
        res = conn.getresponse()
        # return res.read().decode('gb18030')
        str = res.read().decode('gb18030')
        l1 = str.split('=')
        l2 = l1[1].split(',')
        d = {}
        d['name'] = l2[0]
        d['open'] = float(l2[1])
        d['last'] = float(l2[2])
        d['close'] = float(l2[3])
        d['high'] = float(l2[4])
        d['low'] = float(l2[5])
        return d
    except Exception as err:
        print(err)
    finally:
        conn.close()
    return None


if __name__ == '__main__':
    a = ['sh600549', 'sh000001', 'sh601168']
    while True:
        for code in a:
            d = getsinahq(code)
            if d is None:
                continue
            else:
                zf = str(round(100 * (d['close'] - d['last']) / d['last'], 2))
                if d['close'] >= d['last']:
                    print('\033[31m' + d['name'][1:2] + str(round(d['close'], 2)) + '\033[0m')
                    print('\033[31m' + '  ' + zf + '\033[0m')
                else:
                    print('\033[40m' + d['name'][1:2] + str(round(d['close'], 2)) + '\033[0m')
                    print('\033[40m' + '  ' + zf + '\033[0m')
        time.sleep(3)

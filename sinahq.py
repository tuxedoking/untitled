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
    while True:
        #print('\033[31m'+getsinahq('sh600549')['close']+'\033[0m')
        d = getsinahq('sh600549')
        d2 = getsinahq('sh000001')
        if d is None:
            continue
        else:
            if d['close'] >= d['last']:
                print('\033[31m' + str(round(d['close'], 2)) + '\033[0m')
            else:
                print('\033[40m' + str(round(d['close'], 2)) + '\033[0m')

            if d2['close'] >= d2['last']:
                print('\033[31m' + str(round(d2['close'], 2)) + '\033[0m')
            else:
                print('\033[40m' + str(round(d2['close'], 2)) + '\033[0m')
        time.sleep(3)

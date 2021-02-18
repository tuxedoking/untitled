import tsdatasource as tsds
import pymysql
import matplotlib.pyplot as plt


def calfd(n1, n2):
    return (n2 - n1) / n1


def calfd2(n1, n2):
    return abs((n2 - n1) / min(n1, n2))


def getstockweekdata(code):
    try:
        mysql = tsds.mysqlhelper()
        db = mysql.connectmysql()
        mysqlcode = tsds.getmysqlcode(code)
        sql = 'select date,open,high,low,close,vol,amout from weekline2_qfq where obj = \'' \
              + mysqlcode + '\' order by date'
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        arr_lines = []
        for rows in results:
            date = rows[0]
            d2 = {}
            d2['date'] = date
            d2['open'] = rows[1]
            d2['high'] = rows[2]
            d2['low'] = rows[3]
            d2['close'] = rows[4]
            d2['vol'] = rows[5]
            d2['amout'] = rows[6]
            arr_lines.append(d2)
        return arr_lines
    except Exception as err:
        print('error', err)
        return None
    finally:
        db.close()


def getstockdaydata(code):
    try:
        mysql = tsds.mysqlhelper()
        db = mysql.connectmysql()
        mysqlcode = tsds.getmysqlcode(code)
        sql = 'select date,open,high,low,close,vol,amout from dayline2_qfq where obj = \'' \
              + mysqlcode + '\' order by date'
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        arr_lines = []
        for rows in results:
            date = rows[0]
            d2 = {}
            d2['date'] = date
            d2['open'] = rows[1]
            d2['high'] = rows[2]
            d2['low'] = rows[3]
            d2['close'] = rows[4]
            d2['vol'] = rows[5]
            d2['amout'] = rows[6]
            arr_lines.append(d2)
        return arr_lines
    except Exception as err:
        print('error', err)
        return None
    finally:
        if db is not None:
            db.close()


'''
画浪型算法：
1.五根线不创新高，就是下降
2.五根线不创新低，就是上升
'''


def calbolang(lines, fromdate=0, enddate=20500101):
    if enddate <= fromdate:
        return None

    def getpricevol(fromdateindex, todateindex):
        dates = []
        prices = []
        vols = []
        for i in range(fromdateindex, todateindex + 1):
            line = lines[i]
            dates.append(line['date'])
            prices.append(line['close'])
            vols.append(line['vol'])
        return dates, prices, vols

    fromi = 0
    endi = 0
    for i in range(0, len(lines)):
        line = lines[i]
        if line['date'] >= fromdate and fromi == 0:
            fromi = i
        if line['date'] >= enddate:
            endi = i
            break

    if endi == 0:
        endi = len(lines) - 1

    if endi - fromi <= 30:
        print('endi = ', endi, ' fromi = ', fromi)
        return None

    qushifromindex = fromi
    qushitoindex = fromi
    qushi = 0  # 1-上升（横盘即是上升） 2-下降  0-一开始
    nizhuancount = 0
    bolangs = []

    for i in range(fromi + 1, endi + 1):  # len(lines)):
        # print(weeklines[i])

        line = lines[i]
        if line['close'] < lines[qushitoindex]['close']:
            if qushi == 2:
                qushitoindex = i
                nizhuancount = 0
            elif qushi == 1:
                nizhuancount += 1
                if nizhuancount == 5:  # 趋势逆转
                    bolang = {}
                    dates, prices, vols = getpricevol(qushifromindex, qushitoindex)
                    bolang['dates'] = dates
                    bolang['prices'] = prices
                    bolang['vols'] = vols
                    bolang['qushi'] = qushi

                    bolangs.append(bolang)

                    qushifromindex = qushitoindex  # + 1
                    qushitoindex = i
                    qushi = 2
                    nizhuancount = 0
            elif qushi == 0:
                qushi = 2
                qushitoindex = i
                nizhuancount = 0
        else:
            if qushi == 1:
                qushitoindex = i
                nizhuancount = 0
            elif qushi == 2:
                nizhuancount += 1
                if nizhuancount == 5:  # 趋势逆转
                    bolang = {}
                    dates, prices, vols = getpricevol(qushifromindex, qushitoindex)
                    bolang['dates'] = dates
                    bolang['prices'] = prices
                    bolang['vols'] = vols
                    bolang['qushi'] = qushi

                    bolangs.append(bolang)

                    qushifromindex = qushitoindex  # + 1
                    qushitoindex = i
                    qushi = 1
                    nizhuancount = 0
            elif qushi == 0:
                qushi = 1
                qushitoindex = i
                nizhuancount = 0

    dates, prices, vols = getpricevol(qushifromindex, qushitoindex)
    bolang = {}
    bolang['dates'] = dates
    bolang['prices'] = prices
    bolang['vols'] = vols
    bolang['qushi'] = qushi
    bolangs.append(bolang)

    if qushitoindex < endi:  # len(lines) - 1:
        dates, prices, vols = getpricevol(qushitoindex, endi)  # len(lines) - 1)
        bolang = {}
        bolang['dates'] = dates
        bolang['prices'] = prices
        bolang['vols'] = vols
        if qushi == 1:
            bolang['qushi'] = 2
        else:
            bolang['qushi'] = 1
        bolangs.append(bolang)

    return bolangs


def getbolangstezheng(bolangs):
    openprice = bolangs[0]['prices'][0]
    closeprice = bolangs[-1]['prices'][-1]

    blstezheng = {}
    zhangfu = round(calfd(openprice, closeprice), 4)
    if zhangfu == 0:
        zhangfu = 0.0001
    blstezheng['from'] = bolangs[0]['dates'][0]
    blstezheng['to'] = bolangs[-1]['dates'][-1]
    blstezheng['zhangfu'] = zhangfu
    # daycount = 0
    shapes = []

    min = 10000000.0
    max = 0.0

    dayset = set()

    for bolang in bolangs:
        zf = calfd(bolang['prices'][0], bolang['prices'][-1])
        shapes.append((round(zf * 100, 4), len(bolang['dates'])))
        for date in bolang['dates']:
            dayset.add(date)
        # daycount += len(bolang['dates'])
        prices = bolang['prices']
        for price in prices:
            if price > max:
                max = price
            if price < min:
                min = price

    blstezheng['zhenfu'] = round(calfd(min, max), 4)
    blstezheng['daycount'] = len(dayset)
    blstezheng['shapes'] = shapes

    # blstezheng['shapescount'] = len(shapes)
    return blstezheng


def dis_bolangs(blstezheng, blstezheng2):
    zhangfu1 = blstezheng['zhangfu']
    zhangfu2 = blstezheng2['zhangfu']
    if zhangfu1 * zhangfu2 < 0:
        return False
    if calfd2(zhangfu1, zhangfu2) > 0.15:
        return False
    if calfd2(blstezheng['zhenfu'], blstezheng2['zhenfu']) > 0.2:
        return False
    if calfd2(blstezheng['daycount'], blstezheng2['daycount']) > 0.15:
        return False
    # return True
    distance = 0
    for i in range(0, len(blstezheng['shapes'])):
        shape = blstezheng['shapes'][i]
        shape2 = blstezheng2['shapes'][i]
        distance += ((shape[0] - shape2[0]) ** 2 + (0.5 * (shape[1] - shape2[1])) ** 2) ** 0.5
    return round(distance, 4)


def getsimbolang(bolangs, blstezheng):
    firstqushi = 0
    if blstezheng['shapes'][0][0] >= 0:
        firstqushi = 1
    else:
        firstqushi = 2

    ret = []
    for i in range(0, len(bolangs)):
        bolang = bolangs[i]
        bdcount = len(blstezheng['shapes'])
        if i + bdcount > len(bolangs):
            break
        tempbolangs = []
        if bolang['qushi'] == firstqushi:
            for j in range(i, i + bdcount):
                tempbolangs.append(bolangs[j])
            blstezheng2 = getbolangstezheng(tempbolangs)
            distance = dis_bolangs(blstezheng, blstezheng2)
            if distance == False:
                continue
            else:
                # ret.append(tempbolangs)
                ret.append((distance, blstezheng2))
    return ret


def printbolangs(bolangs):
    for bolang in bolangs:
        for key, value in bolang.items():
            if key == 'qushi':
                if value == 1:
                    print('上升趋势')
                else:
                    print('下降趋势')
            else:
                print(key, value)

        print('\n')


def drawbolangs(bolangs):
    plt.subplot(2, 1, 1)
    iii = 0
    for bolang in bolangs:
        x = []
        for i in bolang['dates']:
            x.append(iii)
            iii += 1
        y = []
        for price in bolang['prices']:
            y.append(price)
        if bolang['qushi'] == 1:
            plt.plot(x, y, color='red')
        else:
            plt.plot(x, y, color='green')

    plt.subplot(2, 1, 2)
    iii = 0
    for bolang in bolangs:
        x = []
        for i in bolang['dates']:
            x.append(iii)
            iii += 1
        y = []
        for vol in bolang['vols']:
            y.append(vol / 100000000)
        if bolang['qushi'] == 1:
            plt.bar(x, y, color='red')
        else:
            plt.bar(x, y, color='green')

    plt.show()


if __name__ == '__main__':
    lines = getstockdaydata('002579')
    bolangs = calbolang(lines, fromdate=20190204, enddate=20500211)  # , enddate=20200224)  # 20191112
    # bolangs = bolangs2[-5:]
    # bolangs = bolangs2[1:]
    printbolangs(bolangs)

    blstezheng = getbolangstezheng(bolangs)
    print(blstezheng)

    # drowbolangs(bolangs)
    tsdsi = tsds.tsdatasource()
    codelist = tsdsi.getcodelist()

    l4sort = []
    for code in codelist:
        lines = getstockdaydata(code)
        bolangs = calbolang(lines)
        if bolangs is None:
            continue

        ret = getsimbolang(bolangs, blstezheng)
        # print(code)
        for (distance, blstezheng2) in ret:
            # print(distance)
            # print(bltezheng)
            l4sort.append((distance, code, blstezheng2))
            # print(bolangs)

    l4sort.sort(key=lambda x: x[0])
    for (distance, code, blstezheng2) in l4sort:
        print(code)
        print(distance)
        print(blstezheng2)

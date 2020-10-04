import pymysql


class Mysql_Helper:
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='stock2', autocommit=True)

    def runsql(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    try:
        mh = Mysql_Helper()
    except Exception as err:
        mh.runsql("select 1")


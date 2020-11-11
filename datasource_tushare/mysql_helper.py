import pymysql


class Mysql_Helper:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', port=3306, user='root', password='zhouli20160101', db='stock', autocommit=True)

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


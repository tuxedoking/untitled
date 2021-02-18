import pymysql

if __name__ == '__main__':
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='stock',
                                 autocommit=True)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO a (a) VALUES ('haha3')"
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        #connection.commit()

    finally:
        connection.close()
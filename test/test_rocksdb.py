import rocksdb


db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
#str = '你在干嘛'
#db.put(b'a', bytes(str, encoding='utf8'))
if db.get(bytes('a', encoding='utf8')) is None:
    print('ahhah')
else:
    print(bytes.decode(db.get(b'a'), encoding='utf-8'))

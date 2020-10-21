import rocksdb
import pickle


'''
db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
#str = '你在干嘛'
#db.put(b'a', bytes(str, encoding='utf8'))
if db.get(bytes('a', encoding='utf8')) is None:
    print('ahhah')
else:
    print(bytes.decode(db.get(b'a'), encoding='utf-8'))
'''


if __name__ == '__main__':
    db = rocksdb.DB("../dayline.db", rocksdb.Options(create_if_missing=True))
    it = db.iteritems()
    it.seek_to_first()
    for key, value in it:
        print(str(key, encoding='utf8'))
        lines = pickle.loads(value)
        print(lines)


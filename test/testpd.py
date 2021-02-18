import json


if __name__ == '__main__':
    d = {'a': 3, 'b': '我的'}
    str = json.dumps(d, ensure_ascii=False)
    print(str)
    e = json.loads(str)
    print(e)
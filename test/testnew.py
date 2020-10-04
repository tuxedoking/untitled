class test:
    def __new__(cls):
        self = object.__new__(cls)
        print('__new__')
        return self

    def __init__(self):
        print('__init__')
        self.a = 'sss'

    @classmethod
    def t(cls):
        print(cls.a)


if __name__ == '__main__':
    #t = test()
    #print(t.a)
    test.t()
def change_code2tscode(code):
    if len(code) != 6:
        return None
        #raise OverflowError(code + ',len != 6')
    if code[0:1] == '6':
        return code+'.SH'
    elif code[0:1] == '3' or code[0:1] == '0':
        return code+'.SZ'
    else:
        return None
        #raise ValueError(code + ',value error!')


if __name__ == '__main__':
    try:
        print(change_code2tscode('200123'))
    except Exception as err:
        print(err)
    finally:
        print('hello')
'''
Created on 2019/06/08

@author: aokan
'''
from rakuten_rss import rss


def getRakutenCode(year, month, p_c, sp):
    code = '1'

    if (p_c[0:1] == 'P'):
        code = code + '3'
    elif (p_c[0:1] == 'C'):
        code = code + '4'
    else:
        code = code + '6'

    code = code + str(year - 2015)

    if (month < 10):
        code = code + '0' + str(month)
    else:
        code = code + str(month)

    if (type != 'Stock'):
        thousand = sp // 1000 - (sp // 10000) * 10
        handred = sp // 100 - (sp // 1000) * 10
        code = code + str(thousand) + str(handred) + '18'
    else:
        code = code + '0019'

    if (int(rss(code + '.OS', '権利行使価格')) != sp):
        if (code[1:2] == '9') :
            code = code[0:1] + '4' + code[2:]
        elif (code[1:2] == '8'):
            code = code[0:1] + '3' + code[2:]
        elif (code[1:2] == '4'):
            code = code[0:1] + '9' + code[2:]
        elif (code[1:2] == '3'):
            code = code[0:1] + '8' + code[2:]

    return code


def tr_zn_to_digit(zn):
    d_zn_to_digit = {
        "零": 0,
        "一": 1,
        "二": 2,
        "两": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
        "百": 100,
        "千": 1000,
        "万": 10000,
        "亿": 100000000,
    }
    for e in zn:
        if e not in zn:
            raise ValueError('传入值含未知字符')
    ores = 0
    ures = 0

    o = zn.split('亿')
    if len(o) == 1:
        o = ['', o[0]]
    for i, e in enumerate(o):
        res = 0
        for j, char in enumerate(e):
            if char in d_zn_to_digit:

                if char in '十百千':
                    if not ((j == 0 or e[j - 1] in '零十百千万') and char == '十'):
                        continue
                elif char in '万':
                    res *= d_zn_to_digit[char]
                    continue
                cur_digit = d_zn_to_digit[char]

                if j < len(e) - 1:
                    next_char = e[j + 1]
                    if next_char in '十百千':
                        cur_digit *= d_zn_to_digit[next_char]
                res += cur_digit
        if i == 0:
            ores = res * 100000000
        elif i == 1:
            ures = res
    res = ores + ures

    # print(res)
    return res


def tr_digit_to_zn(digit):
    # 940,2400,0452
    digit = str(digit)
    length = len(digit)
    digit = digit[::-1]
    split = []
    sp_nums = range(0, length, 4)
    for i in sp_nums:
        split.append(digit[i: i + 4][::-1].zfill(4))
    # print(split)
    d_digit_to_zn = {
        0: "零",
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
    }
    res_zn_list = []
    split_count = len(split)
    for i, e in enumerate(split):
        zn = ''
        for j, each in enumerate(e):
            if each == '0':
                if j == 0 and i == split_count - 1:
                    pass
                elif e[j - 1] == '0':
                    pass
                elif e[j:].strip('0'):
                    zn += '零'
            else:
                zn += d_digit_to_zn[int(each)] + {0: '千', 1: '百', 2: '十', 3: ''}[j]
        zn = zn + {0: '', 1: '万', 2: '亿'}[i]
        res_zn_list.append(zn)
    res_zn_list.reverse()
    res_zn = ''.join(res_zn_list)
    # print(res_zn)

    res_zn = [e for e in res_zn]
    for i, e in enumerate(res_zn):
        if e in '百千':
            try:
                if res_zn[i - 1] == '二':
                    res_zn[i - 1] = '两'
            except:
                pass
    res_zn = ''.join(res_zn)

    if res_zn.startswith('一十'):
        res_zn = res_zn[1:]

    if res_zn.startswith('二') and res_zn[1] in ['万','亿']:
        res_zn = '两' + res_zn[1:]

    return res_zn


print(tr_zn_to_digit('十七亿四十三万二千四百二十三'))
print(tr_digit_to_zn(2222222222))
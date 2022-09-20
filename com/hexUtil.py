import binascii


# 测试十六进制字符换 转换需要取出的值
def str2val(reciveData):
    print("recive:" + reciveData)
    array = reciveData.split(" ")
    valArray = []

    for val in array:
        print('val='+val)
        valArray.append(int(val, 16))
    # if len(array) > 2:
    #     print('hexval ' + str(array[-2]))
    #     print('val ' + str(valArray[-2]))
    #     num = float(valArray[-2]) / 10
    #     print('num:%.2f m/s  ' % num)
    for v in valArray:
        s = str(v) + ' '  # string for output
        print('{0}'.format(s), end='')
        # print(' '+str(v))
    return valArray


if __name__ == '__main__':
    # str2val("01 03 00 00 00 02 C4 0B")
    valArray = str2val("01 03 02 00 00 B8 44")

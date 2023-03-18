import serial
import time

speed = "01 03 00 00 00 01 84 0A"           # speed
# ser.port = "/dev/ttyUSB0"
# "COM5"
serial_dev = "/dev/ttyUSB0"
def connectrs485():
    return serial.Serial(serial_dev,
                         baudrate=4800,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1.0)
def read_data():
    winspeed=0

    try:
        ser = connectrs485()
        ser.is_open
    except Exception as ex:
        print("风速仪端口打开失败"+str(ex))
        return
    if ser.is_open:
        print("port open success")
        # hex（16进制）转换为bytes（2进制），应注意python3.7与python2.7此处转换不同
        send_data = bytes.fromhex(speed)  # 发送数据转换为b'\xff\xff\xff\xff\xff'
        ser.write(send_data)  # 发送数据
        time.sleep(0.1)       # 延时，否则len_return_data将返回0
        len_return_data = ser.inWaiting()  # 将获取缓冲数据（接收数据）长度
        # print(len_return_data)
        if len_return_data:
            return_data = ser.read(len_return_data)    # 读取缓冲数据
            # bytes（2进制）转换为hex（16进制），应注意python3.7与python2.7此处转换不同
            str_return_data = str(return_data.hex())
            print(str_return_data)
            winspeed=int(str_return_data[6:10], 16)
            print(str(str_return_data[6:10]))
            print("当前风速为：", end="")
            print(str(winspeed)+"m/s")  # 16进制转为整形   CO值
                # print()
                # if int(str_return_data[6:10], 16) > 50000:
                #     print("当前CO浓度过高！")
                #     temp_GS = 0
        print("port open failed")
        return  winspeed
if __name__ == "__main__":
    while(True):
        read_data()

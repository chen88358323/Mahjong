from time import sleep

import serial  # 导入串口通信库
# https://www.cnblogs.com/L707/p/16364448.html
ser = serial.Serial()


def port_open_recv():  # 对串口的参数进行配置
    # ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)  # 使用USB连接串行口
    # ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)  # 使用树莓派的GPIO口连接串行口
    # ser = serial.Serial(1, 9600, timeout=0.5)  # winsows系统使用com1口连接串行口
    # ser = serial.Serial("COM3", 4800, timeout=0.5)  # winsows系统使用com1口连接串行口
    # ser = serial.Serial("/dev/ttyS1", 9600, timeout=0.5)  # Linux系统使用com1口连接串行口
    ser.port = 'COM3'
    ser.baudrate = 4800
    ser.bytesize = 8
    ser.stopbits = 1
    ser.parity = "N"  # 奇偶校验位
    ser.open()
    if ser.isOpen():
        print("串口打开成功！")
    else:
        print("串口打开失败！")


# isOpen()函数来查看串口的开闭状态
def port_close():
    ser.close()

    if ser.isOpen():

        print("串口关闭失败！")

    else:

        print("串口关闭成功！")


def send(send_data):
    if ser.isOpen():

        ser.write(send_data.encode('utf-8'))  # 编码

        print("发送成功", send_data)

        rslen = ser.inWaiting()
        if rslen != 0:
            response = ser.read(rslen);
            print('返回结果:'+response)
    else:

        print("发送失败！")


if __name__ == '__main__':

    port_open_recv()
    # try:
    while True:
        a = input("输入要发送的数据：")

        send(a)

        sleep(0.5)  # 起到一个延时的效果，这里如果不加上一个while True，程序执行一次就自动跳出了
    # except KeyboardInterrupt:
    #     print("Exiting Program")
    #
    # except Exception as exception_error:
    #     print("Error occurred. Exiting Program")
    #     port_close()
    #     print("Error: " + str(exception_error))
    # finally:
    #     port_close()
    # pass
#

# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial

ser = serial.Serial("/dev/ttyAMA0",9600,timeout=1)
ser.parity = serial.PARITY_EVEN # 奇偶校验设置，在没有交换端口的时候，这里就是错误产生的地方
print(ser.portstr)

command = "hello world"
print("send:" + command)
len = ser.write(command.encode())
print("len = " + str(len))
print("You can always send data, press Ctrl + C to exit")
while 1:
    # strInput = raw_input('enter some words:')  # python2.7的交互方式
    strInput = input('enter some words:')
    print("strencode = " + str(strInput.encode()))
    ser.write(strInput.encode())
ser.flush()
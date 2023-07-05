# -*- coding: utf-8 -*-
import serial
import serial.tools.list_ports
import traceback
def listport():
    plist = list(serial.tools.list_ports.comports())
    ports = [p.name for p in plist]
    print(ports)
def listport2():
    port_list = list(serial.tools.list_ports.comports())
    print(port_list)
def port12():
    portName='/dev/ttyS0'
    ser= serial.Serial(portName,
                         baudrate=9600,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1.0)
    portName = '/dev/ttyS1'
    if ser.is_open:
        print(portName + " is open")
    ser1 = serial.Serial(portName,
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=1.0)
    if ser1.is_open:
        print(portName + " is open")

    portName = '/dev/ttyS2'
    ser2 = serial.Serial(portName,
                         baudrate=9600,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=1.0)


    if ser2.is_open:
        print(portName+" is open")

    print('list port done')
    ser.close()
    ser1.close()
    ser2.close()

if __name__ == '__main__':
    try:
        listport()
        port12()
    except :
        traceback.print_exc()

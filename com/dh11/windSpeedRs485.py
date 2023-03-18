import serial, time

ser = serial.Serial()
# ser.port = "/dev/ttyUSB0"
ser.port = "COM5"
#ls -al /dev/ttyUS*
# 115200,N,8,1
ser.baudrate = 4800
ser.bytesize = serial.EIGHTBITS  # number of bits per bytes
ser.parity = serial.PARITY_NONE  # set parity check
ser.stopbits = serial.STOPBITS_ONE  # number of stop bits

ser.timeout = 0.5  # non-block read 0.5s
ser.writeTimeout = 0.5  # timeout for write 0.5s
ser.xonxoff = False  # disable software flow control
ser.rtscts = False  # disable hardware (RTS/CTS) flow control
ser.dsrdtr = False  # disable hardware (DSR/DTR) flow control


####20,15:08:01.895,RS485ControlV21.exe(12000),IRP_MJ_WRITE,COM5,7,
####	FD FD FD 00 00 E9 88  | ýýý\#0\#0é,
# 21,15:08:01.940,RS485ControlV21.exe(12000),IRP_MJ_READ,COM5,7,
# 	FD FD FD 02 01 29 28  | ýýý\#2\#1)(,
try:
    ser.open()
except Exception as ex:
    print("open serial port error " + str(ex))
    exit()

if ser.isOpen():

    try:
        ser.flushInput()  # flush input buffer
        ser.flushOutput()  # flush output buffer

        # write 8 byte data
        ser.write([78, 78, 78, 78, 78, 78, 78, 78])
        print("write 8 byte data: 78, 78, 78, 78, 78, 78, 78, 78")

        time.sleep(0.5)  # wait 0.5s

        # read 8 byte data
        response = ser.read(8)
        print("read 8 byte data:")
        print(response)

        ser.close()
    except Exception as e1:
        print("communicating error " + str(e1))

else:
    print("open serial port error")
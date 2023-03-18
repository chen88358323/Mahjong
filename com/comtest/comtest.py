#coding:utf-8
#!/usr/bin/python3
import serial
import serial.tools.list_ports
import threading
import time

__all__ = ["CSerial"]

class CSerial:
    def __init__(self, Port, Baud, TimeOut):
        self.l_serial = None
        self.alive = False
        self.waitEnd = None
        self.port = Port
        self.baud = Baud
        self.timeOut = TimeOut
        self.readString = ""
        self.readBin = None
        self.receiveReady = False
        self.thread_SerialRead = None

    def Serial_Create(self):
        try:
            self.l_serial = serial.Serial(self.port, self.baud, timeout=self.timeOut)
        except Exception as e:
            print("serial port error：", e)

    def Serial_WriteAndReadBin(self,bin):
        WaitingCnt = 0
        self.alive = True
        self.l_serial.write(bin)
        while self.alive:
            time.sleep(0.1)   #1 second
            if self.l_serial.in_waiting:
                self.readBin = self.l_serial.read(self.l_serial.in_waiting)
                self.alive = False
                return self.readBin
            else:
                 WaitingCnt += 1
                 if WaitingCnt > 3:
                     return None

        return None

    def Serial_WriteAndReadString(self,string):
        WaitingCnt = 0
        self.readString = ""
        self.alive = True
        self.l_serial.write(string.encode("utf-8"))
        while self.alive:
            time.sleep(0.1)  #1 second
            if self.l_serial.in_waiting:
                self.readString = self.l_serial.read(self.l_serial.in_waiting).decode("utf-8")
                self.alive = False
                return self.readString
            else:
                 WaitingCnt += 1
                 if WaitingCnt > 3:
                     return None

        return None

    def Serial_ReadData(self):
        while self.alive:
            if self.l_serial.in_waiting and self.receiveReady == False:
                self.readData = self.l_serial.read(self.l_serial.in_waiting)
                self.receiveReady = True

    def Serial_WriteString(self,string):
         length = self.l_serial.write(string.encode("utf-8"))
         return length

    def Serial_WriteBin(self,bin):
         length = self.l_serial.write(bin)
         return length

    def Serial_Read(self):
        if self.l_serial.in_waiting:
            STRGLO = self.l_serial.read(self.l_serial.in_waiting).decode("utf-8")
            print(STRGLO)

    def Serial_Close(self):
        self.alive = False
        if self.l_serial.isOpen():
            self.l_serial.close()

#test example
if __name__ == '__main__':
    test = CSerial("COM3",4800,0.5)
    test.Serial_Create()
    print(test.Serial_WriteAndReadString("hello, I am a serial port!\r\n"))
    test.Serial_Close()
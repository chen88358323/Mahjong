import datetime
import schedule
import time
import os
import subprocess

#判断迅雷是否运行
def isThunderProcessRun():
 return "Thunder.exe" in os.popen('tasklist /FI "IMAGENAME eq Thunder.exe"').read()
# 7:00-9:00  20:00-24:00 now work
def checkInHour():
    runFlag=False
    #runFlag=True
    now = datetime.datetime.now()
    hour=now.hour
    print(hour)
    if(1<=hour & hour <=8):
        print ('work time')
        runFlag=True
    elif(10<=hour & hour <21):
        print ('work time')
        runFlag=True
    else:
        print ('not working now')
    return runFlag


def thunderController():
 now = datetime.datetime.now()
 ts = now.strftime('%y-%m-%d %h:%m:%s')
 print('thunderController :', ts)
 #判断运行时间
 workhour=checkInHour()#获取运行时段
 isProcessRun=isThunderProcessRun()
 print('workhour:'+workhour+' runstate:'+isProcessRun)
 if(workhour):#在工作时间内
     if(isProcessRun):
         print('thunder is running')
     else:
         # os.system('H:\t7\Thunder\Program\Thunder.exe')
         os.system('C:\Program Files(x86)\Thunder Network\Thunder\Program\Thunder.exe')



         print('thunder is losting,start thunder')
 else:
     if (isProcessRun):
         print('thunder is running ,need kill')
         output=subprocess.run('taskkill /f /im Thunder.exe',shell=True )
         print(str(output))
     else:
         print('thunder is stopped ')

timer=295
def tasklist():
 #创建一个按秒间隔执行任务
 schedule.every(timer).seconds.do(thunderController)
 while True:
  schedule.run_pending()
  time.sleep(10)
if __name__ == '__main__':
 tasklist()
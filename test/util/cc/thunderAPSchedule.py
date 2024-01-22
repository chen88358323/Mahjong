# -*- coding: utf-8 -*-
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

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
 print('*****************************thunderController :', now)
 #判断运行时间
 workhour=checkInHour()#获取运行时段
 isProcessRun=isThunderProcessRun()
 print('workhour:'+str(workhour)+' runstate:'+str(isProcessRun))
 if(workhour):#在工作时间内
     if(isProcessRun):
         print('thunder is running')
     else:
         # os.system('H:\t7\Thunder\Program\Thunder.exe')
         #os.system("C:\Program Files(x86)\Thunder Network\Thunder\Program\Thunder.exe")
         print('thunder is losting,start thunder')
         output = subprocess.run("C:\Program Files(x86)\Thunder Network\Thunder\Program\Thunder.exe", shell=True)
         print('run cmd '+str(output))


 else:
     if (isProcessRun):
         print('thunder is running ,need kill')
         output=subprocess.run('taskkill /f /im Thunder.exe',shell=True )
         print(str(output))
     else:
         print('thunder is stopped ')

timer=295

def test():
    print('sssssssssssssssssssssssssss')
# def tasklist():
#     # 创建调度器对象
#     scheduler = BlockingScheduler()
#     # 添加定时任务
#     scheduler.add_job(thunderController, 'interval', seconds=100)
#
#     # 启动调度器
#     scheduler.start()
if __name__ == '__main__':
    # 创建调度器对象
    scheduler = BlockingScheduler()

    # 添加定时任务
    scheduler.add_job(thunderController, 'interval', seconds=5)

    # 启动调度器
    scheduler.start()
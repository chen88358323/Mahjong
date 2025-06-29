import os
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
#pip3 install psutil
import psutil
import threading
#判断程序是否运行 由于权限问题，需要在管理员cmd下运行此程序
#processname  like Thunder.exe
def isProcessRun(pname):
 return pname in os.popen('tasklist /FI "IMAGENAME eq '+pname+'"').read()
# 7:00-9:00  20:00-24:00 now work

def query_process(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
            return True
    return  False


def timer_task(process_name, interval):
    timer = threading.Timer(interval, timer_task, [process_name, interval])
    query_process(process_name)
    timer.start()
#
# # 启动定时器，‌例如每5秒查询一次"chrome"进程
# timer_task("chrome", 5)
def check_and_start_process():
    process_full_path=r"C:\SOFT\sunlogin\SunloginClient\SunloginClient.exe"
    process_name = "SunloginClient.exe"

    processRunTag=query_process(process_name)
    if(not processRunTag):#为运行
        print(process_name +" is not running ,now starting")
        output=subprocess.run(process_full_path, shell=True)

        print(str(output))
    else:
        print(process_name+"is running,leave it alone")

    return

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    timer=60*60#一小时进行一次检查

    scheduler.add_job(check_and_start_process, 'interval', seconds=timer,max_instances=4)
    scheduler.start()
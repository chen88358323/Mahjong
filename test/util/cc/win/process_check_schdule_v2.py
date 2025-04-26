import win32api
import win32con
import win32process
import time

def check_thunder():
    try:
        # 尝试通过进程名查找
        processes = win32process.EnumProcesses()
        for pid in processes:
            try:
                hProcess = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
                exe_name = win32process.GetModuleFileNameEx(hProcess, 0)
                if 'thunder.exe' in exe_name.lower():
                    print(f"[{time.ctime()}] thunder.exe 正在运行 (PID: {pid})")
                    return True
            except:
                continue
        return False
    except Exception as e:
        print(f"检查失败: {e}")
        return False

def start_thunder():
    thunder_path = r"D:\t7\ThunderXI-20250323\Thunder\Program\Thunder.exe"
    try:
        win32api.ShellExecute(0, 'open', thunder_path, '', '', 1)
        print(f"[{time.ctime()}] 已启动 thunder.exe")
    except Exception as e:
        print(f"启动失败: {e}")

print("监控中...")
while True:
    if not check_thunder():
        start_thunder()
    time.sleep(300)  # 5分钟 = 300秒

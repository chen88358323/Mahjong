import time
import subprocess
import psutil  # 需要安装: pip install psutil

def check_and_start_thunder():
    """
    检查 thunder.exe 进程是否存在，不存在则启动。
    """
    process_name = "Thunder.exe"
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == process_name.lower():
            found = True
            break

    if not found:
        print(f"{process_name} 进程未找到，尝试启动...")
        try:
            # 替换为你的迅雷可执行文件完整路径
            thunder_executable_path = r"D:\t7\ThunderXI-20250323\Thunder\Program\Thunder.exe"
            subprocess.Popen([thunder_executable_path])
            print(f"{process_name} 启动成功。")
        except FileNotFoundError:
            print(f"错误：迅雷可执行文件 '{thunder_executable_path}' 未找到，请检查路径。")
        except Exception as e:
            print(f"启动 {process_name} 时发生错误：{e}")
    else:
        print(f"{process_name} 进程正在运行。")

if __name__ == "__main__":
    while True:
        check_and_start_thunder()
        time.sleep(5 * 60)  # 每 5 分钟 (5 * 60 秒) 检查一次
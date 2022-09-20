import webbrowser
import os
if __name__ == '__main__':
    with open('D:\\temp\\test.txt') as f:
        for line in f.readlines()  :##readlines(),函数把所有的行都读取进来；
            urk = line.strip(  )##删除行后的换行符，img_file 就是每行的内容啦
            webbrowser.open(urk)
            # os.system("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" urk)

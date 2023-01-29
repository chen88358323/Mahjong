from tkinter import filedialog
from tkinter import messagebox
import PySimpleGUI as sg
import os.path
import xlwt
from moviepy.editor import VideoFileClip


def on_choose_dir():
    path = filedialog.askdirectory()
    list = get_filenames(path)
    make_xlsx(list)
    return path


def get_filenames(path):
    print("获取文件列表", path)
    list = []
    exts = ['.mp4', '.mov', '.mpg', '.mxf']
    for cur_dir, dirs, files in os.walk(path):
        for file in files:
            ext = file[-4:]  # 截取后4位字符作为当前文件的扩展名
            if ext in exts:
                videofile = os.path.join(cur_dir, file)
                list.append(videofile)  # 将视频文件路几个放入数组
    print(list)
    return list


def sec2time(sec):
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    pattern = r'%02d:%02d:%02d'
    return pattern % (h, m, s)


def make_xlsx(list):
    print("制作表格")
    wb = xlwt.Workbook()
    ws = wb.add_sheet("视频列表")
    ws.write(0, 0, '视频名称')
    ws.write(0, 1, '封装格式')
    ws.write(0, 2, '时长')
    ws.write(0, 3, '帧率')
    ws.write(0, 4, '路径')

    total = len(list)
    for k, videofile in enumerate(list):
        rowx = k + 1
        filename = os.path.basename(videofile)
        basename = filename[0:-4]  # 获取文件名称
        ext = filename[-3:]  # 获取扩展名

        clip = VideoFileClip(videofile)
        duration = sec2time(clip.duration)
        fps = round(clip.fps, 3)
        dir = os.path.dirname(videofile)
        clip.close()

        ws.write(rowx, 0, basename)
        ws.write(rowx, 1, ext)
        ws.write(rowx, 2, duration)
        ws.write(rowx, 3, fps)
        ws.write(rowx, 4, dir)

        progress = rowx / total * 100
        update_progress(progress)
    save_info = filedialog.asksaveasfile(mode='w', defaultextension='.xlsx')
    print('选择的存储路径', save_info.name)
    if not save_info.name:
        return
    wb.save(save_info.name)
    messagebox.showinfo('成功', '视频信息已存入表格')


def update_progress(progress):
    window['text'].update('{}%'.format(progress))
    window['progressbar'].UpdateBar(progress)


if __name__ == '__main__':
    print("hello word")
    sg.theme("DarkAmber")
    progressbar = [[sg.ProgressBar(100, key='progressbar')]]
    layout = [
        [sg.Button("选择路径")],
        [sg.Text("任务完成进度"), sg.Text('', key='text')],
        [sg.Frame('进度', layout=progressbar)],
        [sg.Button("关闭")]
    ]
    window = sg.Window("视频文件信息转存表格", layout)
    while True:
        event, values = window.read()
        if event == "选择路径":
            on_choose_dir()
        if event in (None, "关闭"):
            break
        print("You entered ", values[0])
    window.close()

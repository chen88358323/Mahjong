import shutil
import numpy as np
from PIL import Image
import os

def 比较图片大小(dir_image1, dir_image2):
    with open(dir_image1, "rb") as f1:
        size1 = len(f1.read())
    with open(dir_image2, "rb") as f2:
        size2 = len(f2.read())
    if (size1 == size2):
        result = "大小相同"
    else:
        result = "大小不同"
    return result

def 比较图片尺寸(dir_image1, dir_image2):
    image1 = Image.open(dir_image1)
    image2 = Image.open(dir_image2)
    if (image1.size == image2.size):
        result = "尺寸相同"
    else:
        result = "尺寸不同"
    return result

def 比较图片内容(dir_image1, dir_image2):
    image1 = np.array(Image.open(dir_image1))
    image2 = np.array(Image.open(dir_image2))
    if (np.array_equal(image1, image2)):
        result = "内容相同"
    else:
        result = "内容不同"
    return result

def 比较两张图片是否相同(dir_image1, dir_image2):
    # 比较两张图片是否相同
    # 第一步：比较大小是否相同
    # 第二步：比较长和宽是否相同
    # 第三步：比较每个像素是否相同
    # 如果前一步不相同，则两张图片必不相同
    result = "两张图不同"
    大小 = 比较图片大小(dir_image1, dir_image2)
    if (大小 == "大小相同"):
        尺寸 = 比较图片尺寸(dir_image1, dir_image2)
        if (尺寸 == "尺寸相同"):
            内容 = 比较图片内容(dir_image1, dir_image2)
            if (内容 == "内容相同"):
                result = "两张图相同"
    return result
#filePath 待清理路径
#重复数量
def duplicateImageFilter(filePath,duplicateCount):
    save_path = filePath+'\imgs_dir_repeat'  # 空文件夹，用于存储检测到的重复的照片
    os.makedirs(save_path, exist_ok=True)

    # 获取图片列表 file_map，字典{文件路径filename : 文件大小image_size}
    file_map = {}
    image_size = 0
    # 遍历filePath下的文件、文件夹（包括子目录）
    for parent, dirnames, filenames in os.walk(filePath):
        # for dirname in dirnames:
        # print('parent is %s, dirname is %s' % (parent, dirname))
        for filename in filenames:
            # print('parent is %s, filename is %s' % (parent, filename))
            # print('the full name of the file is %s' % os.path.join(parent, filename))
            image_size = os.path.getsize(os.path.join(parent, filename))
            file_map.setdefault(os.path.join(parent, filename), image_size)

    # 获取的图片列表按 文件大小image_size 排序
    file_map = sorted(file_map.items(), key=lambda d: d[1], reverse=False)
    file_list_temp = []
    file_size_list = []
    singal_list = []
    for filename, image_size in file_map:
        if(len(file_list_temp)):#存在值
            if (file_size_list[0] == image_size):
                file_list_temp.append(filename)
                file_size_list.append(image_size)
            if(len(file_list_temp) == duplicateCount)    :#达到规定数值清理

                minfile =min(file_list_temp, key=lambda s: len(s))
                print('mifilename==>'+minfile)
                singal_list.append(minfile)
                file_list_temp.clear()
                file_size_list.clear()
        else:
            file_list_temp.append(filename)
            file_size_list.append(image_size)
    for file in singal_list:
        shutil.move(file,save_path)
                #https://blog.csdn.net/sgzqc/article/details/126733659

    # 取出重复的图片
    # file_repeat = []
    # for currIndex, _ in enumerate(file_list_temp):
    #     dir_image1 = file_list_temp[currIndex]
    #     dir_image2 = file_list_temp[currIndex + 1]
    #     result = 比较两张图片是否相同(dir_image1, dir_image2)
    #     if (result == "两张图相同"):
    #         file_repeat.append(file_list_temp[currIndex + 1])
    #         print("\n相同的图片：", file_list_temp[currIndex], file_list_temp[currIndex + 1])
    #     else:
    #         print('\n不同的图片：', file_list_temp[currIndex], file_list_temp[currIndex + 1])
    #     currIndex += 1
    #     if currIndex >= len(file_list_temp) - 1:
    #         break
    #
    # # 将重复的图片移动到新的文件夹，实现对原文件夹降重
    # for image in file_repeat:
    #     shutil.move(image, save_path)
    #     print("正在移除重复照片：", image)

def move_duplicate_images(source_folder, destination_folder):
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        # 检查文件名是否以 (2).jpg 结尾
        if filename.endswith('(2).jpg'):
            # 构造完整的源文件路径
            src_file_path = os.path.join(source_folder, filename)
            # 构造完整的目标文件路径
            dest_file_path = os.path.join(destination_folder, filename)
            # 移动文件到目标文件夹
            shutil.move(src_file_path, dest_file_path)
            print(f"Moved: {src_file_path} to {dest_file_path}")


if __name__ == '__main__':
    # 指定源文件夹和目标文件夹路径
    source_folder = r'G:\down\0555\b38\un\y\六月无水印福利！露脸熟女天花板！推特高贵极品韵味十足熟女女神【徐娘】私拍福利，充满欲望的鲍鱼自摸\P'  # 替换为你的源文件夹路径
    destination_folder = r'G:\down\0555\b38\un\y\六月无水印福利！露脸熟女天花板！推特高贵极品韵味十足熟女女神【徐娘】私拍福利，充满欲望的鲍鱼自摸\P\dup'  # 替换为你的目标文件夹路径

    # 调用函数移动文件
    move_duplicate_images(source_folder, destination_folder)
    os._exit(0)
    filePath = r'D:\360Downloads\test'  # 要去重的文件夹
    for parent, dirnames, filenames in os.walk(filePath):
        for dir in dirnames:
            fpath=(os.path.join(parent, dir))
            duplicateImageFilter(fpath,6)
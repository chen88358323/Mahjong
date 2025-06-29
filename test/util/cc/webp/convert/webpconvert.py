from PIL import Image
import os

def convert_webp_to_jpg(webp_file, jpg_file):
    with Image.open(webp_file) as img:
        img.convert('RGB').save(jpg_file, 'JPEG')


# 使用函数转换文件

def convertjpgs(dirname):
    for dirpath, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            portion = os.path.splitext(filename)
            if portion[1] == ".webp":
                webpfile=os.path.join(dirpath,filename)
                tempname=portion[0]+'.jpg'
                jpgfile=os.path.join(dirpath,tempname)
                with Image.open(webpfile) as img:
                    img.convert('RGB').save(jpgfile, 'JPEG')

if __name__=='__main__':
    webppath=r'D:\CODE\cms\mcms-dep\template\img\图片素材'
    convertjpgs(webppath)
    # jpgpath='D:\DOC\person\signaturev2.jpg'
    # convert_webp_to_jpg('input.webp', 'output.jpg')
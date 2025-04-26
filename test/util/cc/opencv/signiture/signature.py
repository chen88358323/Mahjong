import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
global img
global point1,point2

def on_mouse(event,x,y,flags,param):
    global img,point1,point2
    img2=img.copy()
    if event==cv2.EVENT_LBUTTONDOWN:#左键点击
        point1=(x,y)
        cv2.circle(img2,point1,10,(0,255,0),5)
        cv2.imshow('image',img2)

    elif event==cv2.EVENT_MOUSEMOVE and (flags&cv2.EVENT_FLAG_LBUTTON):#移动鼠标，左键拖拽
        cv2.rectangle(img2,point1,(x,y),(255,0,0),15)#需要确定的就是矩形的两个点（左上角与右下角），颜色红色，线的类型（不设置就默认）。
        cv2.imshow('image',img2)

    elif event==cv2.EVENT_LBUTTONUP:#左键释放
        point2=(x,y)
        cv2.rectangle(img2,point1,point2,(0,0,255),5)#需要确定的就是矩形的两个点（左上角与右下角），颜色蓝色，线的类型（不设置就默认）。
        cv2.imshow('image',img2)
        min_x=min(point1[0],point2[0])
        min_y=min(point1[1],point2[1])
        width=abs(point1[0]-point2[0])
        height=abs(point1[1]-point2[1])
        cut_img=img[min_y:min_y+height,min_x:min_x+width]
        gen_sig(cut_img)
        # cv2.imwrite('crop_cell_nucleus.tif',cut_img)

def gen_sig(img):
    #设定阈值
    import time
    name = str(time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime()))+'.png'
    temp = img[:][:][0]
    mmax = 0
    mmin = 255
    for i in range(len(temp)):
        for j in  range(len(temp[0])):
            mmax = max(mmax, temp[i][j])
            mmin = min(mmin, temp[i][j])
    thresh = mmax*0.5+mmin*0.5-15

    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    B,G,R = cv2.split(img)

    retval1,R=cv2.threshold(R,thresh,255,cv2.THRESH_BINARY)
    _, Alpha= cv2.threshold(R, thresh, 255, cv2.THRESH_BINARY_INV)

    B2,G2,R2,A2 = cv2.split(result)
    A2 = Alpha
    result = cv2.merge([B2,G2,R2,A2]) #通道合并


    cv2.imwrite(name, result)

def main(path):
    global img
    img=cv2.imread(path)
    cv2.namedWindow('image',0)
    cv2.resizeWindow('image', 700, 900)   # 自己设定窗口图片的大小
    cv2.setMouseCallback('image',on_mouse)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__=='__main__':
    #载入原图，并转化为灰度图像
    jpgpath = 'D:\DOC\person\signaturev2.jpg'
    main(jpgpath)


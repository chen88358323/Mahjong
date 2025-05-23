import cv2
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
        cv2.imwrite('crop_cell_nucleus.tif',cut_img)


def main(picpath):
    global img
    img=cv2.imread(picpath)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',on_mouse)
    cv2.imshow('image',img)
    cv2.waitKey(0)


if __name__=='__main__':
    jpgpath='D:\DOC\person\signaturev2.jpg'
    main(jpgpath)




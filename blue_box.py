# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:19:48 2018

@author: tomat
"""

import numpy as np            
import cv2
 

STANDARDIZATION=0

def D_value(path,STANDARDIZATION):
    img_source=cv2.imread(path,-1)
    h_s,w_s,c_s=img_source.shape    
    rotate_mat=cv2.getRotationMatrix2D((w_s/2,h_s/2),180.5,1)
    reversal_img=cv2.warpAffine(img_source,rotate_mat,(w_s,h_s))
    reversal_img=reversal_img[300:h_s-500,350:w_s-350]

    h,w,c=reversal_img.shape
    
#HSV色彩检测
    HSV=cv2.cvtColor(reversal_img,cv2.COLOR_BGR2HSV)
    lower=np.array([105,120,125])
    upper=np.array([122,255,255])
    box=cv2.inRange(HSV,lower,upper)
##    MORPH OPEN
    s_open=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    morph_open=cv2.morphologyEx(box,cv2.MORPH_OPEN,s_open,1)
##    colfilter_img    
    for i in range(w):
        col=morph_open[:,i]
        pixnum=np.flatnonzero(col).shape[0]
        if pixnum>350:
            morph_open[:,i]=col
        else:
            morph_open[:,i]=0
##    find contours 
    contours,hierarchy_L= cv2.findContours(morph_open,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    area_list=[]
    small_area_index=[]

    for i in range(len(contours)):
        cnt=contours[i]
        #计算面积
        area = cv2.contourArea(cnt)
        area_list.append(area)
        if area <5600:
            small_area_index.append(i)
##去除小面积后的轮廓new_contours    
    for i in small_area_index:
        contours[i]=np.zeros((1),np.int32)
    new_contours=[]
    for cnt in contours:
        if len(cnt.shape)==3:
            new_contours.append(cnt)
##    将所有轮廓点集合并
    if len(new_contours)==0:
        Target=0
        print('Target missing!')
        diff_mm=0
    else:  
        cnts=new_contours[0]#初始化点集
        for i in range(len(new_contours)-1):
            cnts=np.concatenate((cnts,new_contours[i+1]),axis=0)
        ##最小外接矩形
        x_box,y_box,w_box,h_box=cv2.boundingRect(cnts)
        if w_box in range(760,1150):
            Target=1
            print('Target found!')
            ptx=250/w_box
            cv2.rectangle(reversal_img, (x_box,y_box), (x_box+w_box, y_box+h_box), (255,0,255), 3)
            cv2.circle(reversal_img,(x_box,y_box),7,(0,255,0),-1)
            mid=x_box+int(w_box/2)   
            
            if STANDARDIZATION:  #校准
                mid_standard=mid
                w_box_standard=w_box
                standard_data=[mid_standard,w_box_standard]
                np.save('standard_data.npy', standard_data)#存储校准数据
                print('Standardization successful')
                
            standard_data=np.load('standard_data.npy')
            mid_standard=standard_data[0]#标准中线值    
            cv2.line(reversal_img,(mid,0), (mid,h), (0,255,0), 1)               
            cv2.line(reversal_img,(mid_standard,0), (mid_standard,h), (255,0,0), 2)        
            print('standard mid line',mid_standard,'\ncurrent mid line:',mid)    
            diff=mid-mid_standard
            diff_mm=diff*ptx
            diff_mm=("%.2f" % diff_mm)
            print('D-Value:',diff,'pixels\n',diff_mm,'mm')
            cv2.arrowedLine(reversal_img,(mid_standard,300), (mid,300), (255,0,0), 2,1,) 

            text=str(diff_mm)+'mm'
            cv2.putText(reversal_img,text,(int((mid_standard+mid)/2)-90,280),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)           
            cv2.imwrite('result_img.jpg',reversal_img)
        else:
            Target=0
            diff_mm=0
            print('unknown object')
    return Target,diff_mm







if __name__ == '__main__':
    img_source=cv2.imread('D:/python_projects/Blue_box/boximg.jpg',-1)

    h_s,w_s,c_s=img_source.shape    
    rotate_mat=cv2.getRotationMatrix2D((w_s/2,h_s/2),180.5,1)
    reversal_img=cv2.warpAffine(img_source,rotate_mat,(w_s,h_s))
    reversal_img=reversal_img[300:h_s-500,350:w_s-350]
    cv2.namedWindow('reversal_img',0)
    cv2.imshow('reversal_img',reversal_img)
    cv2.waitKey(0)
    h,w,c=reversal_img.shape
    
#HSV色彩检测
    HSV=cv2.cvtColor(reversal_img,cv2.COLOR_BGR2HSV)
#    cv2.namedWindow('HSV',0)
#    cv2.imshow('HSV',HSV)
#    cv2.waitKey(0)
    
    
    lower=np.array([105,120,125])
    upper=np.array([122,255,255])
    box=cv2.inRange(HSV,lower,upper)

#    MORPH OPEN
    s_open=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    morph_open=cv2.morphologyEx(box,cv2.MORPH_OPEN,s_open,1)
    cv2.namedWindow('morph_open',0)
    cv2.imshow('morph_open',morph_open)
    cv2.waitKey(0)
#    cv2.imwrite('bluebox1.jpg',morph_open)
#    
#    
#    colfilter_img    
    for i in range(w):
        col=morph_open[:,i]
        pixnum=np.flatnonzero(col).shape[0]
        if pixnum>400:
            morph_open[:,i]=col
        else:
            morph_open[:,i]=0
    cv2.namedWindow('morph_open1',0)
    cv2.imshow('morph_open1',morph_open)
#    cv2.imwrite('bluebox2.jpg',morph_open)
    cv2.waitKey(0)    

#    find contours 
    contours,hierarchy_L= cv2.findContours(morph_open,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)     
#,hierarchy_L
    area_list=[]
    small_area_index=[]

    for i in range(len(contours)):
        cnt=contours[i]
        #计算面积
        area = cv2.contourArea(cnt)
        area_list.append(area)
        if area <5600:
            small_area_index.append(i)
#去除小面积后的轮廓new_contours    
    for i in small_area_index:
        contours[i]=np.zeros((1),np.int32)
    new_contours=[]
    for cnt in contours:
        if len(cnt.shape)==3:
            new_contours.append(cnt)
    new_contour_img=np.zeros((h,w,c),np.uint8)
    cv2.drawContours(new_contour_img,new_contours, -1, (0,255, 0), 2)
    cv2.namedWindow('new_contour_img',0)
    cv2.imshow('new_contour_img',new_contour_img)
    cv2.waitKey(0)    
#    cv2.imwrite('new_contour_img.jpg',new_contour_img)    

#    将所有轮廓点集合并
    if len(new_contours)==0:
        Target=0
        print('Target missing!')
    else:  
        cnts=new_contours[0]#初始化点集
        for i in range(len(new_contours)-1):
            cnts=np.concatenate((cnts,new_contours[i+1]),axis=0)
    #    convexhull=cv2.convexHull(cnts)   
    #    
    #    img=reversal_img.copy()
    #    for i in range(convexhull.shape[0]-1):
    #        cv2.line(img,(convexhull[i,0,0],convexhull[i,0,1]),
    #                 (convexhull[i+1,0,0],convexhull[i+1,0,1]),(255,0,255),3)
    #    cv2.line(img,(convexhull[convexhull.shape[0]-1,0,0],convexhull[convexhull.shape[0]-1,0,1]),
    #                 (convexhull[0,0,0],convexhull[0,0,1]),(255,0,255),3)
    #    
    #    cv2.namedWindow('convexhull',0)
    #    cv2.imshow('convexhull',img)
    #    cv2.waitKey(0)
        ##最小外接矩形
        x_box,y_box,w_box,h_box=cv2.boundingRect(cnts)
        if w_box in range(760,1160):
            Target=1
            print('Target found!')
            ptx=250/w_box
            cv2.rectangle(reversal_img, (x_box,y_box), (x_box+w_box, y_box+h_box), (255,0,255), 3)
            cv2.circle(reversal_img,(x_box,y_box),7,(0,255,0),-1)
            mid=x_box+int(w_box/2)   
            
            if STANDARDIZATION:  #校准
                mid_standard=mid
                w_box_standard=w_box
                standard_data=[mid_standard,w_box_standard]
                np.save('standard_data.npy', standard_data)#存储校准数据
                print('Standardization successful')
                
            standard_data=np.load('standard_data.npy')
            mid_standard=standard_data[0]#标准中线值    
            cv2.line(reversal_img,(mid,0), (mid,h), (0,255,0), 1)               
            cv2.line(reversal_img,(mid_standard,0), (mid_standard,h), (255,0,0), 2)        
            print('standard mid line',mid_standard,'\ncurrent mid line:',mid)
            diff=mid-mid_standard
            diff_mm=diff*ptx
            diff_mm=("%.2f" % diff_mm)
            print('D-Value:',diff,'pixels\n',diff_mm,'mm')
            cv2.arrowedLine(reversal_img,(mid_standard,300), (mid,300), (255,0,0), 2,1,) 

            text=str(diff_mm)+'mm'
            cv2.putText(reversal_img,text,(int((mid_standard+mid)/2)-90,280),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,0,0),2)
            cv2.namedWindow('rect',0)
            cv2.imshow('rect',reversal_img)
            cv2.waitKey(0)            
#            cv2.imwrite('bluebox.jpg',reversal_img)
        else:
            Target=0
            print('unknown object')



















    cv2.destroyAllWindows()



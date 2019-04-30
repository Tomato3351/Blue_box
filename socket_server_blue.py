import sys
import socket
sys.path.append("../")
sys.path.append("../MvImport")
import hikvisionCamera
import blue_box
import time

#path='D:/python_projects/Blue_box/'
raw_file_path = "AfterConvert_RGB.raw"
img_name='boximg.jpg'

device_list = hikvisionCamera.camera_search()
cam, nPayloadSize = hikvisionCamera.camera_open(device_list, 0)  # 打开相机

###socket 通信
server = socket.socket()
server.bind(("192.168.0.9",41000))
server.listen(5)

while True:
    print("等电话")
    order=input("Any key to continue,q to exit!\n>").strip()##去除字符串首尾空格
    if order=='q' or order=='exit':
        break
    else:
        print('Continue...')    
    
    con,addr = server.accept()
    print("已连接",addr)
    while True:
        try:
        #con 就是客户端连过来，在服务器生成的一个连接实例。
            data = con.recv(1024)
            if not data:
                break
            print('receive:',data)
            if data==b'exit':
                time.sleep(2)
                break
            elif data==b'start':

                start_captureImg = time.perf_counter() 
                hikvisionCamera.stream_start(cam)
                img_data,Frame_num,Width,Height=hikvisionCamera.captureImg_faster(cam,nPayloadSize,raw_file_path,path='',img_name='boximg.jpg')
                print('get one frame! Width:',Width,',Height:',Height)
                hikvisionCamera.stream_stop(cam)
                end_captureImg=time.perf_counter()                 
                print('capturing time:',end_captureImg-start_captureImg)
                
                start_detect = time.perf_counter() 
                Target,diff_mm=blue_box.D_value(img_name,STANDARDIZATION=0)
                send_data=str(str(Target)+','+str(diff_mm))
                print("send_data:",send_data)
                con.send(send_data.encode())
                
                end_detect=time.perf_counter() 
                print('processing time:',end_detect-start_detect)
            else:
                send_data="0"
                print ("send_data:",send_data)
                con.send(send_data.encode())
        except ConnectionResetError as e:
            print("err", e)
            break
        
server.close()
hikvisionCamera.camera_close(cam)#    关闭相机 
##






























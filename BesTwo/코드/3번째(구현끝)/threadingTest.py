import logging
import threading
import time
import datetime
import picamera
import keyboard
import cv2

#카메라 변수에 picamera 세팅 및 동영상 저장 경로 변수 생성
camera = picamera.PiCamera()
savepath = '/home/pi/bestwo/python3/savedVideo'

#영상을 저장하는 기능의 스레드 정의
def thread_function(name):
    #현재 시각 '시-분-초'순으로 변수에 저장
    now = time.strftime('%H-%M-%s',time.localtime(time.time()))
    print(now)
    #녹화 시작. 파일 저장 경로에 /video-시-분-초.h264 의 이름으로 녹화본 저장
    camera.start_recording(output = savepath + '/video' +now+ '.h264')
    #녹화동시에 녹화장면 preview 
    camera.start_preview(fullscreen=False, window=(100,20,640,480))
    
    #1분 간격으로 저장하기 위해 55초쯤에서 녹화 중지, 녹화파일 저장하기 위한 loop장치
    while True:
        nowsec=time.strftime('%S', time.localtime(time.time()))
        print(nowsec)
        time.sleep(1)
        if nowsec=='55':
            break
    camera.stop_preview()
    camera.stop_recording()
    #스레드 시작 후 첫번째 녹화 완료.
    
    #이후 00초~55초간 지속적인 녹화를 위한 loop문 정의
    while True:
        #nowsec변수에 실시간으로 현재시각을 받아서 00초에 녹화 시작
        now = time.strftime('%H-%M-%s',time.localtime(time.time()))
        while True:
            nowsec=time.strftime('%S', time.localtime(time.time()))
            print(nowsec)
            time.sleep(1)
            if nowsec=='00':
                break
        #nowsec 00초에 녹화 시작
        camera.start_recording(output = savepath + '/video' +now+ '.h264')
        camera.start_preview(fullscreen=False, window=(100,20,640,480))
        while True:
            #녹화 중지를 위해 55초를 새는 loop문
            nowsec=time.strftime('%S', time.localtime(time.time()))
            print(nowsec)
            time.sleep(0.5)
            if nowsec=='55':
                break
        #55초째에 loop를 탈출하며 녹화 중지 및 저장
        camera.stop_preview()
        camera.stop_recording()
    
##    while True:
##        now = time.strftime('%H-%M-%s',time.localtime(time.time()))
##        nowsec=time.strftime('%S', time.localtime(time.time()))
##        print("Thread %s: starting", name)
##        camera.start_recording(output = savepath + '/video' +now+ '.h264')
##        camera.start_preview(fullscreen=False, window=(100,20,640,480))  
##        camera.wait_recording(20)
##        print("Thread %s: finishing", name)
##        camera.stop_preview()
##        camera.stop_recording()


#기본 카메라 세팅 및 스레드문 정의
def CameraOn():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
    x = threading.Thread(target=thread_function, args=(1,))
    #스레드 시작
    x.start()
##        x.join()

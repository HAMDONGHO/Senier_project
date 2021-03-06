#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 1: GiGA Genie Keyword Spotting"""

from __future__ import print_function

import time
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws # KWS
import MicrophoneStream as MS
KWSID = ['기가지니', '정호야', '동호야', '사장님']
RATE = 16000
CHUNK = 512

#Raspberry Pi의 GPIO포트 입출력 사용을 위한 기본 세팅
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
LED=7
GPIO.setup(LED, GPIO.OUT)
GPIO.output(7, False)
buzzer=33
GPIO.setup(buzzer,GPIO.OUT)
p=GPIO.PWM(buzzer,100)
GPIO.setup(buzzer, GPIO.IN)


#초기 버튼 상태 세팅
btn_status = False

#버튼 입력 감지시 출력 및 버튼상태 설정 정의
def callback(channel):  
	print("falling edge detected from pin {}".format(channel))
	global btn_status
	btn_status = True
	print(btn_status)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def detect():
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:

			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))

			if (rc == 1):
				MS.play_file("../data/sample_sound.wav")
				return 200

def btn_detect():
	global btn_status
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:
			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			GPIO.output(31, GPIO.LOW)
			if (btn_status == True):
				rc = 1
				btn_status = False			
			if (rc == 1):
				GPIO.output(31, GPIO.HIGH)
				MS.play_file("../data/sample_sound.wav")
				return 200

def test(key_word = '기가지니'):
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n호출어를 불러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

#버튼 입력시 실행할 내용 정의
def btn_test(key_word = '사장님'):
    #버튼 상태 전역변수
	global btn_status
	rc = ktkws.init("../data/kwsmodel.pack")
##	print ('init rc = %d' % (rc))
    #버튼 입력 받을 thread 시작
	rc = ktkws.start()
##	print ('start rc = %d' % (rc))
	print ('\n----------------------------------------------------------\n')
	print ('버튼을 누르시고 말씀하세요~~\n')
	#버튼 입력 대기
	ktkws.set_keyword(KWSID.index(key_word))
	#버튼 입력 감지
	rc = btn_detect()
##	print ('detect rc = %d' % (rc))
##	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
    #버튼 입력 확인 및 종료
	ktkws.stop()
	return rc

#버튼 입력 후 부저 및 LED 제어 정의
def BuzzerOn():
    p.start(100)
    print("buzzer on")
    #0.5초간 부저 ON and OFF 2회 반복
    for i in range(2):
        GPIO.output(7, True)
        GPIO.setup(buzzer,GPIO.OUT)
        time.sleep(0.5)
        GPIO.output(7, False)
        GPIO.setup(buzzer, GPIO.IN)
        time.sleep(0.5)
    
    p.stop()
    GPIO.output(7, False)
    GPIO.setup(buzzer, GPIO.IN)


def main():
	test()

if __name__ == '__main__':
	main()

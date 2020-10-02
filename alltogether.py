from pygame import mixer
import pygame
from aip import AipBodyAnalysis
from aip import AipSpeech
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from PIL import Image
import demjson
import time
import numpy as np
import cv2
cam = cv2.VideoCapture(0)  # 初始化摄像头


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


APP_ID = '17854207'
API_KEY = 'z4nAR54jGLWQg8hazBoXoaCW'
SECRET_KEY = 'x9GaZLGtXzkIYHfnk5iAX2rbZFzBHesr'
client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

SpeechAPP_ID = '17855434'
SpeechAPI_KEY = 'pZZUFc8fDD0Qj9Nog8vWFVpM'
SpeechSECRET_KEY = 'pklp8ZtDsy35vzsaLub1dtkwSulAVXkd'
Speechclient = AipSpeech(SpeechAPP_ID, SpeechAPI_KEY, SpeechSECRET_KEY)
pygame.mixer.init()


def speechsys(content):
    result = Speechclient.synthesis(
        content, 'zh', 1, {'spd': 5, 'vol': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('F:/大二上课程/智能硬件应用实验/实验/res.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('F:/大二上课程/智能硬件应用实验/实验/res.mp3')
    pygame.mixer.music.play(loops=0)


resp = urlopen('http://www.weather.com.cn/weather/101010100.shtml')
soup = BeautifulSoup(resp, 'html.parser')
tagDate = soup.find('ul', class_="t clearfix")
dates = tagDate.h1.string

tagToday = soup.find('p', class_="tem")
try:
    temperatureHigh = tagToday.span.string
except AttributeError as e:
    temperatureHigh = tagToday.find_next('p', class_="tem").span.string

temperatureLow = tagToday.i.string
weather = soup.find('p', class_="wea").string
air = urlopen("http://www.air-level.com/air/beijing/")
vap = BeautifulSoup(air, 'html.parser')
poll = vap.find(class_="aqi-dv").div.span.string
tagWind = soup.find('p', class_="win")
winL = tagWind.i.string
# get all the weather information

'''
print('今天是 '+dates[:3])
print('天气 '+weather)
print('最低温度'+temperatureLow)
print('最高温度'+temperatureHigh)
print('风级'+winL)
print('空气质量 '+poll)


hand={'One':'数字1','Five':'数字5','Fist':'拳头','Ok':'OK',
      'Prayer':'祈祷','Congratulation':'作揖','Honour':'作别',
      'Heart_single':'比心心','Thumb_up':'点赞','Thumb_down':'Diss',
      'ILY':'我爱你','Palm_up':'掌心向上','Heart_1':'双手比心1',
      'Heart_2':'双手比心2','Heart_3':'双手比心3','Two':'数字2',
      'Three':'数字3','Four':'数字4','Six':'数字6','Seven':'数字7',
      'Eight':'数字8','Nine':'数字9','Rock':'Rock','Insult':'竖中指','Face':'脸'}
'''

prevres = 0
while True:
    ret, frame = cam.read()
    cv2.imshow('Original', frame)  # 显示原始图像
    # print(type(frame))
    im = Image.fromarray(frame)
    # print(type(im))
    im.save("exp.jpg")
    image = get_file_content('exp.jpg')
    # print(type(image))
    #image = get_file_content(im)
    # print(client.gesture(image))
    raw = str(client.gesture(image))
    text = demjson.decode(raw)
    try:
        res = text['result'][0]['classname']
    except:
        pass
    else:
        if (res != prevres):
            #print('识别结果：' + hand[res])
            prevres = res
            if(res == 'Insult'):
                print('空气质量 '+poll)
                speechsys('空气质量 '+poll)
            if(res == 'Heart_single'):
                print('天气 '+weather)
                speechsys('天气 '+weather)
            if(res == 'Thumb_up'):
                print('最高温度'+temperatureHigh)
                speechsys('最高温度'+temperatureHigh)
            if(res == 'Thumb_down'):
                print('最低温度'+temperatureLow)
                speechsys('最低温度'+temperatureLow)
            if(res == 'Five'):
                print('风级'+winL)
                speechsys('风级'+winL)
    if cv2.waitKey(1) == 27:  # 等待按键
        break


cv2.destroyAllWindows()
cam.release()

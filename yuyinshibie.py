# -*- coding: utf-8 -*-
 
from aip import AipSpeech  #百度语音识别库
import pyaudio             #麦克风声音采集库
import wave
import requests,json       #音乐搜索
import pygame              #mp3播放
import os
import time
import sys
""" 我的 APPID AK SK """
APP_ID = '17853478' #需要到百度AI注册申请ID  KEY 
API_KEY = 'GUfAa6znHVWmbK6jwCmtoz0R'
SECRET_KEY = 'Azug3qUT2TeybppVMOCqDsZgqUOZ318G'
 
#定义采集声音文件参数
CHUNK = 1024
FORMAT = pyaudio.paInt16 #16位采集
CHANNELS = 1             #单声道
RATE = 16000             #采样率
RECORD_SECONDS = 9       #采样时长 定义为9秒的录音
WAVE_OUTPUT_FILENAME = "/home/pi/my_python_programe/myvoice.pcm"  #采集声音文件存储路径
 
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
 
#获取下载地址
def get_down_url(songid):
    req=requests.get("http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17206073972467458864_1511011710426&songid=%s&_=1511011713541" %songid)
    req.encoding='utf-8'
    #print(json.loads(req.text))
    json1=json.loads(req.text.replace("jQuery17206073972467458864_1511011710426(","").replace(");",""))
    print("下载地址:",json1["bitrate"]['show_link'])
    return json1["bitrate"]['show_link']
#下载保存文件
def music_down(url,music_name,artistname):
    f=open(music_name+'-'+artistname+'.mp3','wb')
    req_mp3=requests.get(url)
    f.write(req_mp3.content)
    f.close()
#调用百度AI，将文字转化为声音输出，用于提示音
def word_to_voice(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/my_python_programe/audio.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('/home/pi/my_python_programe/audio.mp3')#text文字转化的语音文件
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy() == True:
        print('waiting')
 
def word_to_voice1(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/my_python_programe/audio1.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('/home/pi/my_python_programe/audio1.mp3')
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy() == True:
        print('waiting')
 
#获得麦克风输入的声音文件，保存在myvoice.pcm
def  get_mic_voice_file(p):
    word_to_voice('请说出歌名')
 
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")
 
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    #p.terminate()#这里先不使用p.terminate(),否则 p = pyaudio.PyAudio()将失效，还得重新初始化。
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('recording finished')
 
#百度语音识别出歌名文字并返回
def  baidu_get_song_name(client):
    results = client.asr(get_file_content(WAVE_OUTPUT_FILENAME), 'pcm', 16000, { 'dev_pid': 1536, })
    # print(results['result'])
    song_name=results['result'][0]
    print(song_name)
    return song_name
 
#百度音乐下载歌曲，取自百度
def download_music_file(song_name):
    req_url = "http://sug.music.baidu.com/info/suggestion?format=json&word=%s&version=2&from=0&callback=window.baidu.sug&third_type=0&client_type=0&_=1511013032878" % song_name
    req_so = requests.get(req_url)
    data = json.loads(req_so.text.replace("window.baidu.sug(", "").replace(");", ""))
    for i in data["data"]["song"]:
        print("\tsongid:" + str(i["songid"]), "音乐名字:" + i["songname"], "\t歌手:" + i["artistname"])
    input_songid = data["data"]["song"][0]["songid"]  # input("请输入你要下载的songid:")
    for i in data["data"]["song"]:
        if input_songid == str(i["songid"]):
            url = get_down_url(i["songid"])
            music_down(url, i["songname"], i["artistname"])
            print("下载完成")
            music_name = i['songname']  # 获取MP3文件中的歌曲名
            artistname = i["artistname"]  # 获取MP3文件中的歌手名
    filename = '/home/pi/my_python_programe/' + music_name + '-' + artistname + '.mp3'
    print(filename)
 
    word_to_voice1('请欣赏')
    return filename
 
def play_mp3(music_file):
    pygame.mixer.music.load(music_file)
    '''while True:
        # 检查音乐流播放，有返回True，没有返回False
        # 如果一直有音乐流则选择播放
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()'''
    pygame.mixer.music.play(loops=0)  #该函数运行后立即返回，音乐一直在后台运行
 
def one_time_process(p):#一次麦克采样+语音识别+音乐下载+自动播放
    get_mic_voice_file(p)
    play_mp3(download_music_file(baidu_get_song_name(client)))
 
 
 
if __name__=='__main__':
    #麦克风采集初始化、百度语音识别初始化、mp3文件播放初始化
    p = pyaudio.PyAudio()
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    pygame.mixer.init()
    #
 
 
    while 1:#循环调用麦克录音
        one_time_process(p)
        while pygame.mixer.music.get_busy()==True:
            print('playing')
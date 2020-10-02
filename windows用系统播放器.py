# -*- coding: utf-8 -*-

from aip import AipSpeech  # 百度语音识别库
import pyaudio  # 麦克风声音采集库
import wave
import requests
import json  # 音乐搜索
import pygame  # mp3播放
import os
import time
import sys
import re
import urllib
from playsound import playsound
import os

""" 我的 APPID AK SK """
APP_ID = '17853478'  # 需要到百度AI注册申请ID  KEY
API_KEY = 'GUfAa6znHVWmbK6jwCmtoz0R'
SECRET_KEY = 'Azug3qUT2TeybppVMOCqDsZgqUOZ318G'

# 定义采集声音文件参数
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位采集
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率
RECORD_SECONDS = 5  # 采样时长 定义为9秒的录音
WAVE_OUTPUT_FILENAME = "F:/大二上课程/智能硬件应用实验/实验/myvoice.pcm"  # 采集声音文件存储路径


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 调用百度AI，将文字转化为声音输出，用于提示音


def word_to_voice(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('F:/大二上课程/智能硬件应用实验/实验/audio.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('F:/大二上课程/智能硬件应用实验/实验/audio.mp3')  # text文字转化的语音文件
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy() == True:
        print('waiting')


def word_to_voice1(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('F:/大二上课程/智能硬件应用实验/实验/audio1.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('F:/大二上课程/智能硬件应用实验/实验/audio1.mp3')
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy() == True:
        print('waiting')


def word_to_voice2(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('F:/大二上课程/智能硬件应用实验/实验/audio2.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('F:/大二上课程/智能硬件应用实验/实验/audio2.mp3')
    pygame.mixer.music.play(loops=0)
    while pygame.mixer.music.get_busy() == True:
        print('waiting')
# 获得麦克风输入的声音文件，保存在myvoice.pcm


def get_mic_voice_file(p):
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
    # p.terminate()#这里先不使用p.terminate(),否则 p = pyaudio.PyAudio()将失效，还得重新初始化。
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('recording finished')

# 百度语音识别出歌名文字并返回


def baidu_get_song_name(client):
    results = client.asr(get_file_content(
        WAVE_OUTPUT_FILENAME), 'pcm', 16000, {'dev_pid': 1536, })
    if 'result' in results.keys():
        print(results['result'])
        song_name = results['result'][0]
        print(song_name)
        if song_name == "结束程序":
            sys.exit()
        return song_name
    else:
        return "一路向北"


def parse(keyword, num):
    # keyword:要搜索的歌名或者歌手名,num:搜索结果的条数
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song' \
          '&searchid=57124856116396257&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&' \
          'n='+str(num)+'&w='+str(keyword)+'&g_tk=5381&jsonpCallback=MusicJsonCallback3695372008103126' \
          '&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    print(url)
    # 添加user-agent
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

    # 第一次返回：MusicJsonCallback3695372008103126包
    response = requests.get(url, headers=head)
    response = response.text.strip("MusicJsonCallback3695372008103126()[]")

    # 解析json
    json_data = json.loads(response)
    print(json_data)

    json_data = json_data['data']['song']['list']
    print(json_data)
    strMediaMids = []
    songmids = []
    srcs = {}
    songnames = []
    singers = []
    albumns = []
    songid = []
    # 遍历所获取的列表，找到歌曲信息存储在list中
    for data in json_data:
        try:
            strMediaMids.append(data['file']['strMediaMid'])
            songmids.append(data['mid'])
            songnames.append(data['name'])
            singers.append(data['singer'][0]['name'])
            albumns.append(data['album']['name'])
            songid.append(data['id'])
        except:
            print('wrong')

    # 将获取到的信息二次组装成url
    for n in range(0, len(strMediaMids)):

        # 将strMediaMids和songmids重新组合到url中
        url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
            songmids[n] + '&filename=C400' + \
            strMediaMids[n] + '.m4a&guid=6612300644'
        # 获取返回文件并解析得到vkey
        response2 = requests.get(url2)
        json_data2 = json.loads(response2.text)
        vkey = json_data2['data']['items'][0]['vkey']
        # 这是最终的歌曲url
        song_url = 'http://dl.stream.qqmusic.qq.com/C400' + \
            strMediaMids[n] + '.m4a?vkey=' + vkey + \
            '&guid=6612300644&uin=0&fromtag=66'

        # 获取歌词文本
        refer = 'https://y.qq.com/n/yqq/song/' + songmids[n] + '.html'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer': refer}
        lyric_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=' \
                    + str(songid[n]) + '&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        response3 = requests.get(lyric_url, headers=head).text
        json_data3 = response3.strip(' jsonp1()[]')
        print(json_data3)
        jsonp1 = json.loads(json_data3)
        try:
            lyric = jsonp1['lyric']
        except:
            print('wrong')
        # print(lyric)

        # result = re.findall(r'[\u4e00-\u9fa5]+', lyric)
        # lyric = ' '.join(result)
        data = {}
        data['歌手'] = singers[n]
        data['歌名'] = songnames[n]
        data['专辑'] = albumns[n]
        data['url'] = song_url
        data['lyric'] = lyric
        data['songmid'] = songmids[n]
        data['strMediaMids'] = strMediaMids[n]
        data['songid'] = songid[n]
        srcs[n] = data
    with open(str(keyword)+'.json', 'w', encoding='utf-8') as f:
        json.dump(srcs, f)


def download(keyword):
    with open(keyword+'.json', 'r') as f:
        data = json.load(f)
    # print(data)
    for key in data:
        time.sleep(1)
        url = data[key]['url']
        # print(url)
        if os.path.exists(data[key]['歌名']+'.m4a') == False:
            print('正在下载:', data[key]['歌名'], '......')
            try:
                urllib.request.urlretrieve(
                    url, 'F:/大二上课程/智能硬件应用实验/实验/'+data[key]['歌名']+'.m4a')
                # with open(str(data[key]['歌名'])+'-'+str(data[key]['歌手'])+'.m4a','w') as f:
                #     f.write(requests.get(url).content)
            except:
                print('下载'+data[key]['歌名']+'失败')
                word_to_voice2("下载失败")
        else:
            print("歌曲已存在")
    print('下载完成！')

    filename = 'F:/大二上课程/智能硬件应用实验/实验/' + data[key]['歌名']+'.m4a'
    print(filename)

    word_to_voice1('请欣赏')
    return filename


def play_m4a(music_file):
    '''m4a_path = "F:/大二上课程/智能硬件应用实验/实验/" 
    #m4a文件所在文件夹

    m4a_file = os.listdir(m4a_path)

    for i, m4a in enumerate(m4a_file):
        #name = os.path.split(m4a)
        dot = m4a.rfind(".")
        if dot == -1:
            s = ""
        else:
            s = m4a[dot+1:]
        if s=='m4a':
            if os.path.exists(m4a[:dot]+'.mp3')==False:
                os.system("F:/安装程序/实用小软件/ffmpeg-20191125-d5e3d8e-win64-static/bin/ffmpeg -i "+ m4a_path + m4a 
        + " " + m4a_path + m4a[:dot] + ".mp3" )
    dot=music_file.rfind(".")
    music_file=music_file[:dot]+'.mp3'
    pygame.mixer.music.load(music_file)'''
    '''while True:
        # 检查音乐流播放，有返回True，没有返回False
        # 如果一直有音乐流则选择播放
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()'''
    # pygame.mixer.music.play(loops=0)  #该函数运行后立即返回，音乐一直在后台运行
    # playsound(music_file)
    os.system(music_file)


def one_time_process(p):  # 一次麦克采样+语音识别+音乐下载+自动播放
    get_mic_voice_file(p)
    parse(baidu_get_song_name(client), 1)
    play_m4a(download(baidu_get_song_name(client)))


if __name__ == '__main__':
    # 麦克风采集初始化、百度语音识别初始化、mp3文件播放初始化
    p = pyaudio.PyAudio()
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    pygame.mixer.init()

    while 1:  # 循环调用麦克录音
        one_time_process(p)
        # while pygame.mixer.music.get_busy()==True:
        #    print('playing')

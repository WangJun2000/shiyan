import json
import re
import ffmpeg  # 转文件格式
import os  # 调用系统的一些函数
import sys
import time
import urllib
import wave
import pyaudio  # 采集声音的库
import pygame  # 播放mp3文件
import requests  # 爬虫
from aip import AipSpeech  # 语音识别的库
from playsound import playsound

default = 'default'

# 百度的项目id和密码
ID = '17853478'
KEY = 'GUfAa6znHVWmbK6jwCmtoz0R'
KEY2 = 'Azug3qUT2TeybppVMOCqDsZgqUOZ318G'

# 采集声音文件的参数
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16位采集
CHANNELS = 1  # 单声道
RATE = 48000  # 采样率
RECORD_SECONDS = 5  # 采样时长 定义为5秒的录音


def read_file(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 语音转文字
def word_to_voice(text):
    result = client.synthesis(text, 'zh', 1, {'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/Desktop/1800012845/audio.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load(
        '/home/pi/Desktop/1800012845/audio.mp3')  # text文字转化的语音文件
    pygame.mixer.music.play(loops=0)


def word_to_voice1(text):
    result = client.synthesis(text, 'zh', 1, {'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/Desktop/1800012845/audio1.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('/home/pi/Desktop/1800012845/audio1.mp3')
    pygame.mixer.music.play(loops=0)


def word_to_voice2(text):
    result = client.synthesis(text, 'zh', 1, {'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/Desktop/1800012845/audio2.mp3', 'wb') as f:
            f.write(result)
            f.close()
    pygame.mixer.music.load('/home/pi/Desktop/1800012845/audio2.mp3')
    pygame.mixer.music.play(loops=0)


def word_to_voice3(text):
    result = client.synthesis(text, 'zh', 1, {
        'vol': 5, 'spd': 3, 'per': 3})
    if not isinstance(result, dict):
        with open('/home/pi/Desktop/1800012845/audio3.mp3', 'wb') as f:
            f.write(result)
            f.close()
    print(text)


# 采集语音，并转换成pcm文件存储，再转码
def get_voice(p):
    word_to_voice('请说出歌名、歌手或歌词')
    time.sleep(4)
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,input=True, frames_per_buffer=CHUNK)
    print("*开始录制")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*结束录制")
    stream.stop_stream()
    stream.close()
    wf = wave.open("/home/pi/Desktop/1800012845/myvoice.pcm", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    os.system("ffmpeg -y -i " + "/home/pi/Desktop/1800012845/myvoice.pcm" +
              " -ar 16000 "+"/home/pi/Desktop/1800012845/myvoice1.wav")

# 语音转文字


def voice_to_word(client):
    results = client.asr(read_file("/home/pi/Desktop/1800012845/myvoice1.wav"), 'wav', 16000, {'dev_pid': 1536, })
    if 'result' in results.keys():  # 判断是否识别到了读入的语音
        song_name = results['result'][0]
        print(song_name)
        if song_name == "结束程序":
            sys.exit()
        return song_name
    else:
        global default
        print("没有识别到声音")
        if default == 'default':  # 可以手动输入歌曲
            default = input("请输入默认歌曲：")
        return default


def parse(keyword, num):  # 这个函数负责解析
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song' \
          '&searchid=57124856116396257&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&' \
          'n='+str(num)+'&w='+str(keyword)+'&g_tk=5381&jsonpCallback=MusicJsonCallback3695372008103126' \
          '&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    # 添加user-agent
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

    # 第一次返回：MusicJsonCallback3695372008103126包
    response = requests.get(url, headers=head)
    response = response.text.strip("MusicJsonCallback3695372008103126()[]")

    # 解析json
    json_data = json.loads(response)
    json_data = json_data['data']['song']['list']
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
            return

    # 将获取到的信息二次组装成url
    for n in range(0, len(strMediaMids)):
        # 将strMediaMids和songmids重新组合到url中
        url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
            songmids[n] + '&filename=C400' + \
            strMediaMids[n] + '.m4a&guid=6612300644'
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
        jsonp1 = json.loads(json_data3)
        try:
            lyric = jsonp1['lyric']
        except:
            print('wrong')
            return

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
    with open('/home/pi/Desktop/1800012845/music/'+str(keyword)+'.json', 'w', encoding='utf-8') as f:  # 存储json文件
        json.dump(srcs, f)


def download(keyword):
    global default
    try:
        with open('/home/pi/Desktop/1800012845/music/'+keyword+'.json', 'r') as f:
            data = json.load(f)
        for key in data:
            time.sleep(1)
            url = data[key]['url']
            # 判断这首歌有没有
            if os.path.exists('/home/pi/Desktop/1800012845/music/'+data[key]['歌名']+'.m4a') == False:
                print('正在下载:', data[key]['歌名'], '......')
                try:
                    urllib.request.urlretrieve(
                        url, '/home/pi/Desktop/1800012845/music/'+data[key]['歌名']+'.m4a')
                    print('下载完成！')
                except:
                    print('下载'+data[key]['歌名']+'失败')
                    if default == keyword:
                        default = "default"
                    word_to_voice2('下载'+data[key]['歌名']+'失败')
                    time.sleep(2.5)
                    word_to_voice3("请换一首歌")
                    return '/home/pi/Desktop/1800012845/audio3.py'
            else:
                print("歌曲已存在")

        filename = '/home/pi/Desktop/1800012845/music/' + \
            data[key]['歌名']+'.m4a'
        print(filename)

        return filename
    except:
        word_to_voice3("没有这首歌曲，请说出下一首")
        return '/home/pi/Desktop/1800012845/audio3.py'


volume = 0.2  # 这是一个全局变量


def play_music(music_file):
    global volume
    m4a_path = "/home/pi/Desktop/1800012845/music/"  # m4a文件所在文件夹

    m4a_file = os.listdir(m4a_path)

    for i, m4a in enumerate(m4a_file):  # 这是转码的过程，需要将文件的空格先去掉，转码后再加回来
        temp = m4a
        dot1 = temp.rfind(".")
        m4a = m4a.translate(str.maketrans('', '', ' '))
        dot = m4a.rfind(".")
        if dot == -1:
            s = ""
        else:
            s = m4a[dot+1:]
        if s == 'm4a':
            if os.path.exists('/home/pi/Desktop/1800012845/music/'+temp[:dot1]+'.mp3') == False:
                if temp != m4a:
                    os.rename(m4a_path+temp, m4a_path+m4a)
                os.system("ffmpeg -i " + m4a_path + m4a
                          + " " + m4a_path + m4a[:dot] + ".mp3")
                if temp != m4a:
                    os.rename(m4a_path+m4a, m4a_path+temp)
                    os.rename(m4a_path+m4a[:dot] + ".mp3",
                              m4a_path+temp[:dot1] + ".mp3")

    dot = music_file.rfind(".")
    music_file = music_file[:dot]+'.mp3'
    word_to_voice1('请欣赏')
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=0)


def do_it_once(p):  # 一次成功的执行
    get_voice(p)
    songname = voice_to_word(client)
    parse(songname, 1)
    play_music(download(songname))


if __name__ == '__main__':
    p = pyaudio.PyAudio()  # 初始化
    client = AipSpeech(ID, KEY, KEY2)
    pygame.mixer.init()

    while 1:  # 循环
        do_it_once(p)
        while pygame.mixer.music.get_busy() == True:
            print('''
*****************************
* 1.新的曲目   2.退出程序    *
* 3.暂停播放   4.取消暂停    *
* 5.音量调大   6.音量调小    *
*****************************
            ''')
            s = input("请选择您要操作的序号：")
            if s == '1':
                print("新的曲目")
                break
            elif s == '2':
                print("退出程序")
                sys.exit()
            elif s == '3':
                print("暂停播放")
                pygame.mixer.music.pause()
            elif s == '4':
                print("取消暂停")
                pygame.mixer.music.unpause()
            elif s == '5':
                print("音量调大")
                if volume >= 1:
                    print("已经是最大音量了")
                else:
                    volume += 0.1
                    pygame.mixer.music.set_volume(volume)
            elif s == '6':
                print("音量调小")
                if volume <= 0:
                    print("已经是最小音量了")
                else:
                    volume -= 0.1
                    pygame.mixer.music.set_volume(volume)
            elif s == '7':
                default = "default"
                break
            else:
                print("无效指令")
            print("当前音量："+str(round(pygame.mixer.music.get_volume(), 1)))

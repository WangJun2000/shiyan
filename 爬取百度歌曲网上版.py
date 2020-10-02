#encoding=utf-8
#-*- encoding : utf-8 -*-
#/python-pachong/music-baidu/music_spider.py
#爬百度音乐上面的文件信息----------------搜索音乐，并输出前几首，然后由用户指定下载。。。
import requests
import re
import json
import os
 
# data = {
#     'key': '刘德华'
# }
# search_url = 'http://music.baidu.com/search?key='
key = raw_input("请输入想要获取对应音乐的的歌手:"),
 
ids = {0,20,40}
data = {
    'key': key,
           #"刘德华"
           #"王力宏"
           #"Declan Galbraith",
    's': 1,
    # 'start': ','.join(str(ids)),
    'start': 0,
    'size': 20,
    'third_type': 0,
}
 
search_url = 'http://music.taihe.com/search/song'
search_response = requests.get(search_url,params=data)
# print type(search_response)
search_response.encoding="utf-8"
 
search_html = search_response.text
 
# print search_html
song_ids = re.findall(r'sid&quot;:(\d+),', search_html)
data = {
    'songIds': ','.join(song_ids),
    'hq': 0,
    'type': 'm4a,mp3',
    'pt': 0,
    'flag': -1,
    's2p': -1,
    'prerate': -1,
    'bwt': -1,
    'dur': -1,
    'bat': -1,
    'bp': -1,
    'pos': -1,
    'auto': -1,
}
song_link = 'http://play.taihe.com/data/music/songlink'
song_response = requests.post(song_link, data=data)
# 将返回的数据转换为字典
# print song_response
song_info = song_response.json()
# print song_info
song_info = song_info['data']['songList']
# print song_info
# 遍历数组，获取其中的歌曲名称和链接
i = 1
print ("开始下载歌曲...")
for song in song_info:
    print ("正在现在第%d首歌曲\t歌曲名称为:%s" % (i, song['songName']),
    i =i+ 1
    song_name = song['songName']
    singer_name = song['artistName']
    song_lrc = song['lrcLink']
    print song_lrc
 
    #判断歌词文件url是否为空，如果为空，那么将url地址设置为空
    # if (song_lrc == ""):
    #     song_lrc="暂无歌词"
 
    #创建一个以歌手名称命名的文件夹
    if not os.path.exists('music/%s' %singer_name):
        os.mkdir('music/%s' %singer_name)
 
    with open('music/%s/%s_%s.mp3' % (singer_name, song_name, singer_name), "wb") as f:
        if song['songLink'] != "":
            response = requests.get(song['songLink'])
            f.write(response.content)
            f.close()
    with open('music/%s/%s_%s.lrc' % (singer_name, song_name, singer_name), 'wb') as f1:
        if song_lrc != '':
            response = requests.get(song_lrc)
            f1.write(response.content)
            f1.close()
        else:
            f1.write('此歌曲暂无歌词')
            f1.close()
    print "%s*********下载完毕" % song['songName']

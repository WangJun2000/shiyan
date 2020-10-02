import pygame
import time
import os


def welcome():
    print('''
    ***********************
    *                     *
    *   欢迎来到酷我播放器 *
    *                     *
    ***********************
    ''')


def select():
    print('''
    *****************************
    * 1.上一曲      2.下一曲     *
    * 3.暂停播放   4.取消暂停     *
    * 5.音量调大   6.音量调小    *
    * 7.退出      0.播放当前音乐 *
    *****************************
    ''')
    num = input("请选择您要操作的序号：")
    return num


def playMusic(path, volue=0.5):
    pygame.mixer.init()  # 初始化音频
    pygame.mixer.music.load(path)  # 加载路径
    pygame.mixer.music.set_volume(volue)  # 设置音量
    pygame.mixer.music.play()  # 播放


def upMusic(index, musicList):
    if index <= 0:
        print("已经是第一首音乐了")
    else:
        index -= 1
    playMusic(musicList[index])
    return index


def downMusic(index, musicList):
    if index >= len(musicList)-1:
        print("已经是最后一首音乐了")
    else:
        index += 1
        playMusic(musicList[index])
    return index


def pauseMusic():  # 暂停播放。
    pygame.mixer.music.pause()


def unpauseMusic():  # 取消暂停
    pygame.mixer.music.unpause()


def nowMusic():  # 播放当前音乐
    playMusic(musicList[index])


welcome()
volue = 0.5  # 设置起始音量
index = 0  # 设置播放音乐下标
while True:
    time.sleep(1)  # 每次睡眠一秒
    num = select()
    musicList = []  # 存放音乐路径
    path = r"F:\大二上课程\智能硬件应用实验\音乐列表"  # 设置音乐地址
    filepath = os.listdir(path)  # 通过音乐地址获取所有的音乐文件
    for file in filepath:  # 遍历我们的文件列表
        dot = file.rfind(".")
        if dot == -1:
            s = ""
        else:
            s = file[dot+1:]
        if s == 'mp3':
            # 音乐文件路径拼接，拼接为绝对路径，放在musicList中
            musicList.append(os.path.join(path, file))
    print(musicList)
    if num == "0":
        print("播放当前音乐")
        nowMusic()
    elif num == "1":
        print("上一曲")
        index = upMusic(index, musicList)
    elif num == "2":
        print("下一曲")
        index = downMusic(index, musicList)
    elif num == "3":
        print("暂停播放")
        pauseMusic()
    elif num == "4":
        print("取消暂停")
        unpauseMusic()
    elif num == "5":
        print("音量调大")
        if volue >= 1:
            print("已经是最大音量了")
        else:
            volue += 0.1
            pygame.mixer.music.set_volume(volue)
    elif num == "6":
        print("音量调小")
        if volue <= 0:
            print("已经是最小音量了")
        else:
            volue -= 0.1
            pygame.mixer.music.set_volume(volue)
    elif num == "7":
        print("退出")
        break
    print(pygame.mixer.music.get_volume())  # 打印增加或者减少的音量

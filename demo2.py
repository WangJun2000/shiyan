import time
import os, sys
import pygame

def resource_path(relative_path):
    """
    定义一个读取相对路径的函数
      """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    print (base_path)
    return os.path.join(base_path, relative_path)


def music():
    """
    定义一个播放音乐的函数
    :return:
    """
    pygame.mixer.init()
    print("播放音乐1")
    track = pygame.mixer.music.load(resource_path('audio.mp3'))
    pygame.mixer.music.play()
    # print("播放音乐2")
    # track1 = pygame.mixer.music.load("xx.mp3")
    # pygame.mixer.music.play()
    #
    # print("播放音乐3")
    # track2 = pygame.mixer.Sound("tkzc.wav")
    # track2.play()


def timer(n):
    '''''
    每n秒执行一次
    '''
    while True:
        print(time.strftime('%Y-%m-%d %X', time.localtime()))
        start()  # 此处为要执行的任务
        time.sleep(n)


def start():
    print('开始执行mp3文件')
    music()  # 播放音乐了
    print('mp3文件执行完毕')


timer(10)
import pygame
import os
from threading import *
import threading
import time
from PIL import ImageTk, Image
import sys
import tkinter as tk
from tkinter import *
import tkinter.filedialog

filePath = '/home/pi/Desktop/1800012845/music/'  # 音乐存储的地址
file = os.listdir(filePath)
SongName = []
SongPath = []

num = 1

for i in file:  # 把mp3文件添加到播放列表
    dot = i.rfind(".")
    if i[dot+1:] == 'mp3':
        print(num, ":", i[:dot])
        num += 1
        SongName.append(i)
        SongPath.append(filePath+i)
if len(SongName) == 0:  # 没有音乐的情况
    print("该文件夹没有音乐")
    sys.exit()

Number = -1  # 初始化全局变量的数值
volume = 0.3
start = 1
Switch = False


def fun1():  # 下一曲
    global Number
    global Switch
    global start
    Number = Number+1
    if Number > len(SongPath)-1:
        Number = 0
    Switch = False
    start = 0
    pygame.mixer.music.load(SongPath[Number])
    pygame.mixer.music.play(-1)
    entry_var.set(SongName[Number])
    pass


def fun2():  # 暂停/播放
    global start
    global Number
    global Switch
    if start == 1:
        pygame.mixer.music.load(SongPath[0])
        pygame.mixer.music.play(-1)
        Number = 1
        entry_var.set(SongName[0])
        start = 0
    else:
        pygame.mixer.music.set_volume(volume)
        if Switch == True:
            pygame.mixer.music.unpause()
            Switch = False
        else:
            pygame.mixer.music.pause()
            Switch = True

    pass


def fun3():  # 上一曲
    global Number
    global Switch
    global start
    Number = Number-1
    if Number < 0:
        Number = len(SongPath)-1
    start = 0
    Switch = False
    pygame.mixer.music.load(SongPath[Number])
    pygame.mixer.music.play(-1)
    entry_var.set(SongName[Number])

    pass


def fun4():  # 声音调大
    global volume
    volume += 0.1
    if volume > 1:
        volume = 1
    pygame.mixer.music.set_volume(volume)


def fun5():  # 调小
    global volume
    volume -= 0.1
    if volume < 0:
        volume = 0
    pygame.mixer.music.set_volume(volume)


# 制作计时器（这是网上的代码）
def os(time):
    if time < 10:
        return "0"+str(time)
    else:
        return str(time)


def clock(seconds):
    if seconds >= 60:
        minutes = seconds//60
        seconds = seconds-minutes*60
        return os(minutes)+":"+os(seconds)
    else:
        return "00:"+os(seconds)


class Current_time(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        pass

    def clock(seconds):
        if seconds >= 60:
            minutes = seconds//60
            seconds = seconds-minutes*60
            return os(minutes)+":"+os(seconds)
        else:
            return "00:"+os(seconds)

    def run(self):
        while 1:
            playtime = pygame.mixer.music.get_pos()
            seconds = int(playtime)//1000

            current_time = clock(seconds)
            entry_var1.set(current_time)
            time.sleep(1)


root = tk.Tk()
root.title('音乐播放器')  # 创建标题
root["height"] = 150
root["width"] = 300
root.resizable(0, 0)

lal = tk.Label(root, text="欢迎使用音乐播放器")  # 文本框，在root中创建标签
lal.place(x=50, y=15, width=200, height=50)  # 向root放置标签


entry_var = tk.StringVar()
entry_var.set('欢迎使用')
en1 = tk.Entry(root, textvariable=entry_var, justify=CENTER, state=NORMAL)
en1.place(x=50, y=70, width=200, height=15)

entry_var1 = tk.StringVar()
entry_var1.set('00:00')  # 初始声音
en2 = tk.Entry(root, textvariable=entry_var1, justify=CENTER)
en2.place(x=10, y=5, width=80, height=15)


b3 = tk.Button(root, text="+", command=fun4)  # 切换音量
b3.place(x=50, y=90)

b3 = tk.Button(root, text="-", command=fun5)
b3.place(x=65, y=90)

# 1.上一曲按钮
b1 = tk.Button(root, text="上一曲", command=fun3)
b1.place(x=80, y=90)


# 2.播放按钮
b1 = tk.Button(root, text="播放|暂停", command=fun2)  # 定义：按钮名称+按钮功能
b1.place(x=130, y=90)  # 定义：按钮大小+按钮位置

# 3.下一曲按钮
b3 = tk.Button(root, text="下一曲", command=fun1)
b3.place(x=195, y=90)

pygame.mixer.init()
t = Current_time()
t.start()
root.mainloop()

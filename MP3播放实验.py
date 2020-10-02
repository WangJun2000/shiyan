import pygame,sys
import time
from playsound import playsound
def play_mp3(music_file):
    pygame.mixer.music.load(music_file)
    '''while True:
        # 检查音乐流播放，有返回True，没有返回False
        # 如果一直有音乐流则选择播放
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()'''
    pygame.mixer.music.play(loops=0)  #该函数运行后立即返回，音乐一直在后台运行
    time.sleep(5)
    #while pygame.mixer.music.get_busy() == True:
    #    print('waiting')
    #playsound(music_file)
pygame.mixer.init()
play_mp3('F:/大二上课程/智能硬件应用实验/实验/audio.mp3')
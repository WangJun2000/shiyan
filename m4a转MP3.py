# _*_ encoding:utf-8 _*_
import os

m4a_path = "F:/大二上课程/智能硬件应用实验/音乐列表/"
# m4a文件所在文件夹

m4a_file = os.listdir(m4a_path)

for i, m4a in enumerate(m4a_file):
    #name = os.path.split(m4a)
    dot = m4a.rfind(".")
    if dot == -1:
        s = ""
    else:
        s = m4a[dot+1:]
    if s == 'm4a':
        if os.path.exists(m4a[:dot]+'.mp3') == False:
            os.system("F:/安装程序/实用小软件/ffmpeg-20191125-d5e3d8e-win64-static/bin/ffmpeg -i " + m4a_path + m4a
                      + " " + m4a_path + m4a[:dot] + ".mp3")

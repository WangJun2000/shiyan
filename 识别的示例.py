from aip import AipSpeech
import os

""" 你的 APPID AK SK """
APP_ID = '16815394'
API_KEY = 'jM4b8GIG9gzrzySTRq3szK2E'
SECRET_KEY = 'iE626cEpjT1iAVwh24XV5h1QFuR8FPD2'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def read_file(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
# 读取文件
def get_file_content(filePath):

    #文件格式转换成pcm(前提是需要安装ffmpeg软件并配置环境变量)
    pcm_filePath = filePath.split('.')[0] + '.pcm'
    #cmd_str=f'ffmpeg -y  -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {pcm_filePath}'
    #os.system(cmd_str)#调用os.system()在CMD执行命令
    filePath=pcm_filePath

    with open(filePath, 'rb') as fp:
        return fp.read()


# 识别本地文件
result = client.asr(read_file("F:/大二上课程/智能硬件应用实验/实验/myvoice1.wav"), 'wav', 16000, {'dev_pid': 1536, })
print (type(result))
for i in result.keys():
    print(i)
text=result.get('result')[0]

print(result)

print(text)

'''
asr函数需要四个参数,第四个参数可以忽略,自有默认值,参照一下这些参数是做什么的

第一个参数: speech 音频文件流 建立包含语音内容的Buffer对象, 语音文件的格式，pcm 或者 wav 或者 amr。(虽说支持这么多格式,但是只有pcm的支持是最好的)

第二个参数: format 文件的格式,包括pcm（不压缩）、wav、amr (虽说支持这么多格式,但是只有pcm的支持是最好的)

第三个参数: rate 音频文件采样率 如果使用刚刚的FFmpeg的命令转换的,你的pcm文件就是16000

第四个参数: dev_pid 音频文件语言id 默认1537（普通话 输入法模型）
'''
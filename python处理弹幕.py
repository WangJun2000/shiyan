import requests
import win32com.client
import time

old_list = []
#创建一个old_list列表用于辅助后面的text_danmu方法提取新消息
class Danmu():
#定义一个Danmu类
    def __init__(self):
        self.url = "https://api.live.bilibili.com/ajax/msg"
        self.headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0",
            "Referer": "https://live.bilibili.com/284165?spm_id_from=333.334.b_62696c695f6c697665.13",
            }
        self.data = {
            "roomid":"5441",
            "csrf_token":"",	
            "csrf":"",	
            "visit_id":""
            }
        #在 __init__方法中先定义好要使用的请求url,请求头，和请求参数
    def speak_text(self,text):
    #定义一个speak_text方法，并创建形参text，用于作为接下来读取的文字
        speak = win32com.client.Dispatch("SAPI.SpVoice")
        #创建发声对象
        speak.Speak(text)
        #使用发生对象读取文字
        
    def text_danmu(self,html):
    #创建一个text_danmu方法，用于提取弹幕信息
        global old_list
        #设置变量作用域，使得该方法可以修改全局变量old_list的值
        temp_list = []
        #创建一个temp_list列表用于作为临时列表辅助提取弹幕消息
        for text in html["data"]["room"]:
        #for循环提取html字典中嵌套的子字典data中嵌套的子字典room的内容赋值给text变量
        #这个html字典来自于get_danmu方法传递
            temp_list.append(text["text"])
            #将变量text字典中text键的值添加到temp_list中
        if temp_list == old_list:
            pass
        #检测temp_list临时列表的内容和old_list是否相同，如果相同则跳过
        else:
            for text_number in range (1,11):
            #创建for循环一次将1到10的数字赋给text_number
                if "".join(temp_list[:text_number]) in "".join(old_list):
                    pass
                #使用join方法以""为分割符提取temp_list切割后的列表的内容
                #使用join方法以""为分割符提取old_list列表的内容
                #比较内容是否相同，如果相同则跳过
                else:
                    try:
                        print (temp_list[text_number-1])
                    except:
                        pass
                    else:
                        self.speak_text(temp_list[text_number-1])
                    #尝试打印temp_list指定索引的内容，如果报错则跳过
                    #否则调用speak_text方法，进行文字转语言
            old_list = temp_list[:]
            #将temp_list的值赋给old_list，进行更新旧信息列表
            
    def get_danmu(self):
        html = requests.post(url=self.url,headers=self.headers,data=self.data)
        html.json()
        self.text_danmu(eval(html.text))
    #定义get_danmu方法
    #使用requests.post方法获取网页内容
    #将网页返回值以json的信息加载
    #调用之前定义的text_danmu方法，传递eval处理后的网页返回值的文本内容
bzhan = Danmu()
#创建一个bzhan实例
while True:
    bzhan.get_danmu()
    time.sleep(3)
    #每三秒钟调用一个bzhan实例的get_danmu方法


# 子线程监听键盘输入；
# 输入s，暂停，等待输入；输入c，继续；
import time
import threading
import sys

class tt(threading.Thread):
    i = 2
    input_str = ""

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for j in range(0,4):
            input_kb = str(sys.stdin.readline()).strip("\n")
            if input_kb == 's':  # stop
                self.i = 1
                print("子进程捕获了s")
            elif input_kb == "c":  # continue
                self.i = 0
                print("子进程捕获了c")
                self.input_str = input_kb
            else:
                self.input_str = input_kb


def main():
    my_t = tt()
    my_t.start()
    i = 0

    while True:
        if my_t.i == 1:
            while 1:
                print(my_t.i)
                input("请输入：")
                print("my_t.input_str"+my_t.input_str)
                if my_t.input_str == "->":
                    i += 1
                    print(i)
                elif my_t.input_str == "<-":
                    i -= 1
                    print(i)
                elif my_t.input_str == "c":
                    break
        my_t.i = 2
        i += 1
        print('hello', str(i))
        time.sleep(1)


main()

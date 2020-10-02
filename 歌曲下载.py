import sys
import requests

# 屏蔽warning信息，因为下面verify=False会报警告信息
#requests.packages.urllib3.disable_warnings()


def download(url, file_path):
    headers = {
        'Range': 'bytes=0-',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    # verify=False 这一句是为了有的网站证书问题，为True会报错
    r = requests.get(url, headers=headers, stream=True, verify=False)

    # 既然要实现下载进度，那就要知道你文件大小啊，下面这句就是得到总大小
    total_size = int(r.headers['Content-Length'])
    temp_size = 0

    with open(file_path, "wb") as f:
        # iter_content()函数就是得到文件的内容，
        # 有些人下载文件很大怎么办，内存都装不下怎么办？
        # 那就要指定chunk_size=1024，大小自己设置，
        # 意思是下载一点写一点到磁盘。
        for chunk in r.iter_content(chunk_size=2048):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                #############花哨的下载进度部分###############
                done = int(50 * temp_size / total_size)
                # 调用标准输出刷新命令行，看到\r回车符了吧
                # 相当于把每一行重新刷新一遍
                sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符，执行完后需要换行了，不然都在一行显示

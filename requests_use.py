import json
import requests
def parse(keyword, num):
    # keyword:要搜索的歌名或者歌手名,num:搜索结果的条数
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song' \
          '&searchid=57124856116396257&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&' \
          'n='+str(num)+'&w='+str(keyword)+'&g_tk=5381&jsonpCallback=MusicJsonCallback3695372008103126' \
          '&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
    # print(url)
    # 添加user-agent
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

    # 第一次返回：MusicJsonCallback3695372008103126包
    response = requests.get(url, headers=head)
    response = response.text.strip("MusicJsonCallback3695372008103126()[]")

    # 解析json
    json_data = json.loads(response)
    print(json_data)

    json_data = json_data['data']['song']['list']
    # print(json_data)
    strMediaMids = []
    songmids = []
    srcs = {}
    songnames = []
    singers = []
    albumns = []
    songid = []
    # 遍历所获取的列表，找到歌曲信息存储在list中
    for data in json_data:
        try:
            strMediaMids.append(data['file']['strMediaMid'])
            songmids.append(data['mid'])
            songnames.append(data['name'])
            singers.append(data['singer'][0]['name'])
            albumns.append(data['album']['name'])
            songid.append(data['id'])
        except:
            print('wrong')
            return

    # 将获取到的信息二次组装成url
    for n in range(0, len(strMediaMids)):

        # 将strMediaMids和songmids重新组合到url中
        url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=' + \
            songmids[n] + '&filename=C400' + \
            strMediaMids[n] + '.m4a&guid=6612300644'
        # 获取返回文件并解析得到vkey
        response2 = requests.get(url2)
        json_data2 = json.loads(response2.text)
        vkey = json_data2['data']['items'][0]['vkey']
        # 这是最终的歌曲url
        song_url = 'http://dl.stream.qqmusic.qq.com/C400' + \
            strMediaMids[n] + '.m4a?vkey=' + vkey + \
            '&guid=6612300644&uin=0&fromtag=66'

        # 获取歌词文本
        refer = 'https://y.qq.com/n/yqq/song/' + songmids[n] + '.html'
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Referer': refer}
        lyric_url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=' \
                    + str(songid[n]) + '&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        response3 = requests.get(lyric_url, headers=head).text
        json_data3 = response3.strip(' jsonp1()[]')
        # print(json_data3)
        jsonp1 = json.loads(json_data3)
        try:
            lyric = jsonp1['lyric']
        except:
            print('wrong')
            return
        # print(lyric)

        # result = re.findall(r'[\u4e00-\u9fa5]+', lyric)
        # lyric = ' '.join(result)
        data = {}
        data['歌手'] = singers[n]
        data['歌名'] = songnames[n]
        data['专辑'] = albumns[n]
        data['url'] = song_url
        data['lyric'] = lyric
        data['songmid'] = songmids[n]
        data['strMediaMids'] = strMediaMids[n]
        data['songid'] = songid[n]
        srcs[n] = data
    with open('G:/CloudMusic/'+str(keyword)+'.json', 'w', encoding='utf-8') as f:
        json.dump(srcs, f)

parse("周杰伦",1)
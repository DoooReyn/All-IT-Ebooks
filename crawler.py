from requests_html import HTMLSession
import requests
import time
import json
import random
import sys
import re

session = HTMLSession()
pool_url = []
list_url = 'http://www.allitebooks.org/page/'

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

# 获取当前列表页所有图书链接


def get_list(url):
    response = session.get(url)
    all_link = response.html.find('.entry-title a')  # 获取页面所有图书详情链接
    for link in all_link:
        getBookUrl(link.attrs['href'])

# 获取图书下载链接


def getBookUrl(url):
    response = session.get(url)
    l = response.html.find('.download-links a', first=True)
    if l is not None:  # 运行后发现有的个别页面没有下载链接，这里加个判断
        link = l.attrs['href']
        # 添加到下载列表
        pool_url.append(link)
        print(link)
        # download(link)

# 下载图书


def download(url):
    # 随机浏览器 User-Agent
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    # 获取文件名
    filename = url.split('/')[-1]
    # 如果 url 里包含 .pdf
    if ".pdf" in url or ".epub" in url:
        file = 'books/'+filename  # 文件路径写死了，运行时当前目录必须有名 book 的文件夹
        with open(file, 'wb') as f:
            print("正在下载 %s" % filename)
            response = requests.get(url, stream=True, headers=headers)

            # 获取文件大小
            total_length = response.headers.get('content-length')
            # 如果文件大小不存在，则直接写入返回的文本
            if total_length is None:
                f.write(response.content)
            else:
                # 下载进度条
                dl = 0
                total_length = int(total_length)  # 文件大小
                # 每次响应获取 4096 字节
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" %
                                     ('=' * done, ' ' * (50-done)))  # 打印进度条
                    sys.stdout.flush()

            print(filename + '下载完成！')


if __name__ == '__main__':
    response = session.get('http://www.allitebooks.org/page/1')
    links = response.html.links
    max = 0
    for link in links:
        if re.search(list_url, link):
            m = re.match(r'http://www.allitebooks.org/page/(\d+)/', link)
            num = int(m.groups()[0])
            max = num > max and num or max

    # 从这运行，应为知道列表总数，所以偷个懒直接开始循环
    print('总页面:' + str(max))
    for x in range(1, max + 1):
        print('当前页面: ' + str(x))
        get_list(list_url + str(x))

    with open('./urls.txt', 'wt') as f:
        f.writelines([url+'\n' for url in pool_url])

import os
from sys import stdout
import random
import requests
import subprocess

PROGRESS = 64
CHUNK_SIZE = 256
FILE_EXT = ['.pdf', '.epub']
URL_PATH = './urls.txt'
SAVE_PATH = './books/'
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
    'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
]


def getUrls():
    with open(URL_PATH, 'rt') as f:
        urls = f.readlines()
        return [url.rstrip() for url in urls]


def checkUrl(url):
    for ext in FILE_EXT:
        if ext in url:
            return True
    return False


def download(url):
    filename = url.split('/')[-1]
    filepath = os.path.join(SAVE_PATH, filename)
    if os.path.exists(filepath):
        print('《%s》已存在，跳过' % filename)
        return

    if not checkUrl(url):
        return

    with open(filepath, 'wb') as f:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = requests.get(url, stream=True, headers=headers)
        filesize = int(response.headers.get('content-length'))
        print('正在下载 《%s》[%sM] ' % (filename, filesize // 1024 ** 2))
        if filesize is None:
            f.write(response.content)
            return
        downloaded = 0
        for data in response.iter_content(chunk_size=CHUNK_SIZE):
            downloaded += len(data)
            f.write(data)
            done = PROGRESS * downloaded // filesize
            # 打印进度条
            pro = '\r[%s%s]' % ('=' * done, ' ' * (PROGRESS - done))
            stdout.write(pro)
            stdout.flush()
        print('《%s》下载完成！' % filename)


if __name__ == '__main__':
    with open(URL_PATH, 'rt') as f:
        urls = f.readlines()
        for url in urls:
            download(url.rstrip())

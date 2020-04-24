
URL_PATH = './urls.txt'
README_PATH = './README.md'
FILE_EXT = ['.pdf', '.epub']

def checkUrl(url):
    for ext in FILE_EXT:
        if ext in url:
            return True
    return False

if __name__ == '__main__':
    books = ['# All IT Ebooks\n\n']
    with open(URL_PATH, 'rt') as f:
        urls = f.readlines()
        for url in urls:
            url = url.rstrip()
            if checkUrl(url):
                title = url.split('/')[-1].replace('.epub', '').replace('.pdf', '')
                books.append('- [%s](%s)\n' % (title, url.replace(' ', '%20')))
        with open(README_PATH, 'wt') as wf:
            wf.writelines(books)

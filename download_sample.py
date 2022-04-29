import urllib.request

from benchmark import time_elapsed


@time_elapsed
def download(url):
    filename = url[url.rfind('/') + 1:]
    data = urllib.request.urlopen(url).read()
    with open(filename, mode="wb") as f:
        f.write(data)


if __name__ == '__main__':
    url = 'https://ftp.kddilabs.jp/Linux/distributions/knoppix/KNOPPIX_V9.1CD-2021-01-25-EN.iso'
    download(url)

#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://atmarkit.itmedia.co.jp/ait/articles/1911/05/news020.html
import urllib.request

from benchmark import time_elapsed


@time_elapsed
def download(url):
    filename = url[url.rfind('/') + 1:]
    status = True
    try:
        with urllib.request.urlopen(url) as fsrc, open(filename, 'wb') as fdst:
            try:
                content = fsrc.read()
                fdst.write(content)
            except Exception as e:
                print(e)
                status = False
    except OSError as e:
        print(e)
        status = False
    return status


if __name__ == '__main__':
    url = 'https://ftp.kddilabs.jp/Linux/distributions/knoppix/KNOPPIX_V9.1CD-2021-01-25-EN.iso'
    result = download(url)
    print(result)

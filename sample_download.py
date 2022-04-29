#!/usr/bin/env python
# coding: utf-8
# Reference:
# https://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file
import shutil
import urllib.request

from benchmark import time_elapsed


@time_elapsed
def download(url):
    filename = url[url.rfind('/') + 1:]
    status = True
    length = 16 * 1024
    try:
        req = urllib.request.urlopen(url)
        with open(filename, 'wb') as fp:
            try:
                shutil.copyfileobj(req, fp, length)
            except Exception as e:
                print(e)
                status = False
    except OSError as e:
        print(e)
        status = False

    return status


if __name__ == '__main__':
    url = 'https://ftp.kddilabs.jp/Linux/distributions/PLD/iso/2.0/i386/pld-2.0-MINI.i386.iso'
    result = download(url)
    print(result)

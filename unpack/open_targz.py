# -*- coding: utf-8 -*-
# encoding=utf8
import tarfile
import os
import codecs

# python2.7不能解析中文路径，所以以下函数将字符解码
def decode_file_names(tarinfo):
    try:
        tarinfo.name = tarinfo.name.decode('gbk')
    except UnicodeDecodeError:
        tarinfo.name = tarinfo.name.decode('utf-8')
    return tarinfo


def open_targz(filename):
    tar = tarfile.open(filename, mode = "r:gz") #"r:gz"表示 open for reading with gzip compression
    tar.extractall(path='../unpack_file',members=map(decode_file_names, tar)) # 将tar.gz文件解压到指定文件夹下
    tar.close()


if __name__ == '__main__':
    tar_path = '../test.tar.gz'
    open_targz(tar_path)

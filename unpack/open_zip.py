# -*- coding: utf-8 -*-
# encoding=utf8
import zipfile

def open_zip(zip_path):
    zip_file = zipfile.ZipFile(zip_path)
    # extractall()方法从 ZIP 文件中解压缩所有文件和文件夹，放到当前工作目录中
    # 解压可以向 extractall()传递的一个文件夹名称，它将文件解压缩到那个文件夹，而不是当前工作目录
    # 如果传递给 extractall()方法的文件夹不存在，它会被创建
    zip_extract = zip_file.extractall('../unpack_file')
    zip_file.close()

if __name__ == '__main__':
    open_zip('../data.zip')
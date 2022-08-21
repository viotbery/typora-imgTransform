# -*- coding: utf-8 -*-
from urllib import request
import regex as re
import os
from tkinter import *
import requests
# 匹配文档中图片插入的序号，正则表达式(?<=!\[.*?\]\[)\d*(?=\])
# 匹配图片链接注释的正则：(?<=\[\d*\]:\s+).*
def transform(src, out, info, subLink):
    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # 反向读取，从最后一行开始读取
        links = {}
        newLines = ''
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            
            # 匹配文档末尾的图片链接，如[1]: links 中的'links'
            link = re.findall(r'(?<=\[\d*\]:\s+).*', line)
            index = None
            if link:
                # 若匹配到则将该链接按照其序号存入字典中
                index = re.findall(r'(?<=^\[)\d*(?=\])', line)[0]
                r = requests.get(link[0])
                fileName = r.headers['Content-Disposition'].split("'")[-1]
                links[str(index)] = subLink + fileName
                info.insert(END, '成功修改链接：%s\n' % (subLink + fileName))
                # 并将该行删除
                lines[i] = ''
            # 匹配文档中的插入图片的序号，如![1]
            num = re.findall(r'(?<=!\[.*?\]\[)\d*(?=\])', line)
            if num:
                # 若该行是图片插入语法，则将改行内的图片标注替换为图片链接
                # 即由 ![图片注释][图片序号] ===> ![图片注释](图片链接)
                imgIndex = str(num[0])
                lines[i] = re.sub('(?<=!\[.*?\])\[\d*\]','(' + links[imgIndex] + ')', line)
                info.insert(END, '成功替换图片链接：%s\n' % links[imgIndex])
        # 另存为新文件
        fpath, srcName = os.path.split(src)
        with open(out + '/new_' + srcName, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return links

def transformRun(src, out, info, * links):
    subLink = None
    if links[0]:
        subLink = links[1]
    if not (src and out):
        info.insert(END, '错误:文件路径不能为空！\n')
        return
    if os.path.isdir(src):
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.endswith('.md'):
                    info.insert(END, '开始处理文件：%s\n' % file)
                    transform(root + '/' + file, out, info, subLink)
    if os.path.isfile(src):
        transform(src, out, info, subLink)
    info.insert(END, '处理完成！\n')

if __name__ == '__main__':
    info = Text(width=50, height=10)
    transformRun('src/input', 'src/out', info, True, 'https://markdown-img-1311240910.cos.ap-nanjing.myqcloud.com/')

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import filedialog
from transform import transformRun
#@author: viotbery
#@date: 2022-08-20
#@description: 对markdown文件中插入图片的格式进行中转换
#markdown文件中插入图片的格式是：![图片注释][图片序号]，因此需要将其转换为：![图片注释](图片链接)

window = Tk()
window.geometry('500x500')
window.geometry('+700+250')
window.title('markdown图片格式语法转换器')
window.resizable(False, False)

srcFilePath = Label(window,text="输入要转换的文件路径",font=("微软雅黑",10),padx=10, pady=10)

srcFilePathEntry = Entry(window,font=("微软雅黑",10))

outFilePath = Label(window,text="输出文件夹",font=("微软雅黑",10),padx=10, pady=10)

outFilePathEntry = Entry(window,font=("微软雅黑",10))

def selectFile(filePathEntry, isDir=False):
    filePathEntry.delete(0,END)
    if filePathEntry == outFilePathEntry:
        filePathEntry.insert(0,filedialog.askdirectory())
    else:
        if isDir:
            filePathEntry.insert(0,filedialog.askdirectory())
        else:
            filePathEntry.insert(0,filedialog.askopenfilename(filetypes= [('markdown文件', '*.md'),('文本文档', '.txt')]))

srcFilePathSelect = Button(window,text="选择文件夹",font=("微软雅黑",10), height=1, width=10,command=lambda: selectFile(srcFilePathEntry, True))

srcFileDirSelect = Button(window,text="选择文件",font=("微软雅黑",10), height=1, width=10,command=lambda: selectFile(srcFilePathEntry))

outFilePathSelect = Button(window,text="选择文件夹",font=("微软雅黑",10), height=1, width=10,command=lambda: selectFile(outFilePathEntry))

info = Text(window,font=("微软雅黑",10),height=5,width=50,spacing3=5, padx=20, pady=20)

# 添加滚动条
scroll = Scrollbar()

scroll.config(command=info.yview)
info.config(yscrollcommand=scroll.set)
run = Button(window,text="开始转换",font=("微软雅黑",10), height=1, width=10, command=lambda: transformRun(srcFilePathEntry.get(), outFilePathEntry.get(),info))

srcFilePath.grid(row=0,column=0)
srcFilePathEntry.grid(row=1,column=0)
srcFilePathSelect.grid(row=1,column=1, padx=0)
srcFileDirSelect.grid(row=1,column=2, padx=0)

outFilePath.grid(row=2,column=0)
outFilePathEntry.grid(row=3,column=0)
outFilePathSelect.grid(row=3,column=1, pady=10)


info.grid(row=4,column=0, columnspan=3, padx=15)
scroll.grid(row=4,column=4,sticky=N+S)
run.grid(row=5,column=1, pady=5)

window.mainloop()
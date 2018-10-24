# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@
'''
import re, os, time
import datetime


def url2pdf(filePath, startLine, endLine):
    '''
    @ 通过(title : url)文档打印为pdf文档
    @
    @ return
    @
    @ param
    @ exception
    @ notice 
    '''
    url2pdfStart = datetime.datetime.now()
    cnt = 0
    for line in open(filePath):
        start = time.time()
        cnt = cnt + 1
        if ((cnt < startLine) | (cnt > endLine)):
            continue
        print(line)

        pdfName = line.split(' : ', 2)[0] + ".pdf"
        pdfName = pdfName.replace('(','_')
        pdfName = pdfName.replace(')','_')
        pdfName = pdfName.replace('|','_')
        pdfName = pdfName.replace(' ','_')
        wkhUrl2pdfLinux(line.split(' : ', 2)[1], os.path.dirname(filePath)+'/'+pdfName)

        end = time.time()
        print('-----Take time:%s' % str(end - start))

    #统计耗时
    url2pdfEnd = datetime.datetime.now()
    timeDelta = (url2pdfEnd - url2pdfStart).seconds
    print('Total time: ' + str(int(timeDelta / 3600)) + 'h' + str(int(timeDelta / 60) % 60) + 'm' + str((timeDelta % 60)) + 's')   # 时间差

def wkhUrl2pdfLinux(url, pdfName):
    '''
    @ 通过(title : url)文档打印为pdf文档
    @ * 为了解决wkhtmltopdf部分图片失真的问题，把网页中所有的图片保存到本地并用convert转换格式，修改html img src路径为本地绝对路径
    @
    @ return
    @
    @ param
    @ exception
    @ notice 需要安装wkhtmltopdf工具，需要linux环境
    '''

    import urllib.request
    import os,sys
    os.chdir(sys.path[0])
    fileDir = os.path.abspath(os.path.dirname(pdfName)) #获取目录的绝对路径
    fileName = '{}/tmp.html'.format(fileDir)
    html = urllib.request.urlopen(url).read().decode("UTF-8") #read出的是bytes，使用前需要转换为str类型
    pattern = re.compile(r'data-src=\"http.*?\"')  # 用?来控制正则贪婪和非贪婪匹配;(.*?) 小括号来控制是否包含匹配的关键字
    result = pattern.findall(html)

    picCnt = 0
    for i in result:
        picCnt = picCnt + 1
        url = re.findall(r'\"(.*?)\"', i)[0]
        print(url)
        html = html.replace(url, '{}/{}.png'.format(fileDir, str(picCnt)))
        picName = '{}/{}.png'.format(fileDir, str(picCnt))
        os.system('wget {} -O {}'.format(url, picName))
        convertCmd = 'convert {}[0] {}'.format(picName, picName)
        print(convertCmd)
        os.system(convertCmd)
    html = html.replace('data-src','src')
    fd = open(fileName, 'w', encoding="utf-8")
    fd.write(html)
    fd.close()

    os.system('wkhtmltopdf --enable-plugins --enable-forms {} {}'.format(fileName, pdfName))
    os.remove(fileName)
    os.system('rm {}/*.png'.format(fileDir))
    print("下载成功")
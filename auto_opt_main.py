# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@   sudo apt-get install python3-pip
@
'''

def main():
    print("main start")
    caseFlg = 'getGzh2Pdf'
    print(caseFlg)

    if(caseFlg == 'getGzh2Pdf'):
        from android_wechat.get_gzh_essay_spider import gzhEssaySpider
        from url2pdf import url2pdf
        '''
        @ 抓取步骤：1.通过carles+手机获取目标公众号header并修改gzhEssaySpider
        @          2.根据不同需求修改如下3个参数
        '''
        startNum = 0
        endNum = 10000
        gzhName = 'shenmidechengxuyuanmen'

        indexFile='out/{gzhName}/{gzhName}.txt'.format(gzhName=gzhName)
        gzhEssaySpider().spider_more(startNum, endNum, indexFile)
        url2pdf.url2pdf(indexFile, startNum, endNum)


if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    main()


#!/usr/bin/env python
# encoding: utf-8

import requests
import html
import json
import logging
import time,os

class gzhEssaySpider(object):
    def __init__(self):
        # 注意：根据自己抓取的头做相应的修改，微信安全性导致url_more、Cookie经常失效，需要重新请求更换
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; PRO 5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044504 Mobile Safari/537.36 MMWEBID/8780 MicroMessenger/7.0.3.1400(0x2700033A) Process/toolsmp NetType/WIFI Language/zh_CN',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'wxuin=945482497; devicetype=android-24; lang=zh_CN; version=2700033a; pass_ticket=z1xdA4x6PgjBUId//PELAHJScpJt8jeLgfvjH0H6TlO81+hhXVufOv21UP9jM8Wa; wap_sid2=CIHW68IDElxucUV5T01pdFVuaG5ZYWdQVTJlWWE4dndjVkpSbHJBN0daeWJuck5fdW5TZkI4WDdVekhLZjBGdEd5cFE5Yi1oS25jc2FDZjF5QkhSdlRvN0RjdkZPZWNEQUFBfjDEgIfkBTgNQJVO',
            'Accept': '*/*',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MjE4NDEzMg==&scene=126&bizpsid=0&devicetype=android-24&version=2700033a&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=z1xdA4x6PgjBUId%2F%2FPELAHJScpJt8jeLgfvjH0H6TlO81%2BhhXVufOv21UP9jM8Wa&wx_header=1'
        }

        # 更多文章 URL
        # # 注意：请将appmsg_token和pass_ticket替换成你自己的
        self.url_more = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MjE4NDEzMg==&f=json&offset={}&count=10&is_ok=1&scene=126&uin=777&key=777&pass_ticket=z1xdA4x6PgjBUId%2F%2FPELAHJScpJt8jeLgfvjH0H6TlO81%2BhhXVufOv21UP9jM8Wa&wxtoken=&appmsg_token=999_BtKP333DueIFti6oQyU5Dn7x_YFqU6c9agdgOw~~&x5=1&f=json'

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def spider_more(self, offsetStart, offsetEnd, filePath):
        """
        爬取更多数据
        offset：消息索引
        :return:
        """
        current_request_url = self.url_more.format(offsetStart)
        self.logger.info('当前请求的地址是:%s' % (current_request_url))

        response = requests.get(current_request_url, headers=self.headers, verify=False)
        result = response.json()

        if result.get("ret") == 0:
            msg_list = result.get('general_msg_list')

            # 保存数据
            self._save(msg_list, filePath)
            self.logger.info("获取到一页数据成功, data=%s" % (msg_list))

            # 获取下一页数据
            has_next_page = result.get('can_msg_continue')
            next_offset = offsetStart
            if (has_next_page == 1 and next_offset < offsetEnd):
                # 继续爬取写一页的数据【通过next_offset】
                next_offset = result.get('next_offset')

                # 休眠2秒，继续爬下一页
                time.sleep(2)
                self.spider_more(next_offset,offsetEnd, filePath)
            else:  # 当 has_next 为 0 时，说明已经到了最后一页，这时才算爬完了一个公众号的所有历史文章
                print('爬取公号完成！')
        else:
            self.logger.info('无法获取到更多内容，请更新cookie或其他请求头信息')

    def _save(self, msg_list, filePath):
        """
        数据解析
        :param msg_list:
        :return:
        """
        # 1.去掉多余的斜线,使【链接地址】可用
        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)

        # 2.获取列表数据
        msg_list = data.get("list")
        for msg in msg_list:
            # 3.发布时间
            p_date = msg.get('comm_msg_info').get('datetime')

            # 注意：非图文消息没有此字段
            msg_info = msg.get("app_msg_ext_info")

            if msg_info:  # 图文消息
                # 如果是多图文推送，把第二条第三条也保存
                multi_msg_info = msg_info.get("multi_app_msg_item_list")

                # 如果是多图文，就从multi_msg_info中获取数据插入；反之直接从app_msg_ext_info中插入
                if multi_msg_info:
                    for multi_msg_item in multi_msg_info:
                        self._insert(filePath, multi_msg_item, p_date)
                else:
                    self._insert(filePath, msg_info, p_date)
            else:
                # 非图文消息
                # 转换为字符串再打印出来
                self.logger.warning(u"此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    def _insert(self, fileName, msg_info, p_date):
        """
        数据插入到 MongoDB 数据库中
        :param msg_info:
        :param p_date:
        :return:
        """
        keys = ['title', 'author', 'content_url', 'digest', 'cover', 'source_url']

        # 获取有用的数据,构建数据模型
        data = self.sub_dict(msg_info, keys)

        # 时间格式化
        date_pretty = time.strftime('%Y%m%d',time.localtime(p_date))
        print(date_pretty + str(data))
        title = data['title']
        title = title.replace('(','-')
        title = title.replace(')','-')
        title = title.replace('|','-')
        title = title.replace(' ','-')
        title = title.replace('/','-')
        title = title.replace('*','-')
        title = title.replace('\\','-')
        title = title.replace('.','-')
        fileDir = os.path.dirname(fileName)
        if not (os.path.isdir(fileDir)):
            os.system('mkdir -p {}'.format(fileDir))
        fh = open(fileName, 'a+', encoding='utf-8')
        fh.write('{}_{} : {}\n'.format(date_pretty, title, data['content_url']))
        fh.close()

        # 保存数据
        '''
        try:
            post.save()
        except Exception as e:
            self.logger.error("保存失败 data=%s" % post.to_json(), exc_info=True)
        '''
    # ==============================================================================================
    def sub_dict(self, data, keys):
        """
        取字典中有用的数据出来
        获取字典的子字典可以用字典推导式实现
        :param data:字典
        :param keys:键值列表
        :return:有用的键值组成的字典
        """
        return {k: html.unescape(data[k]) for k in data if k in keys}
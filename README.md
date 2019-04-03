# Transform articles in wechat to pdf

现在微信公众号有很多高质量的文章输出，是我们学习的好地方，但手机看太零散，又不方便查找，从而想到将微信公众号的文章导出为PDF可以方便查阅学习。

## 原理：

1.　通过手机抓包获取微信公众号历史文章的  “ 日期_标题：链接 ” 。

2.　通过wkhtmltopdf将网页转换为pdf。

## 准备工作：

1.　需要一部手机，安装微信，
2.　需要一部电脑，目前仅支持 ubuntu，安装抓包工具 Charles；

##  步骤：

1.　从 Git 上面 Clone 本库，在 tools 文件夹中有 wkhtmltopdf 安装包。
2.　让手机和电脑连上同一个 Wifi ，手机上 Wifi 的高级设置将自己的电脑设置为代理服务器里面：
   - 主机名设置为自己电脑的IP地址
   - 端口设置为8888。
3.　打开 Charles, 注意这个时候如果连接正常，Chalres 会提示有设备连接。如果没有，说明可能没有配置正确，需要查询网络上其他的指导文章，了解如何用 Charles 作为手机发信的过滤器。这一步骤比较专业，可参考：
   1.　https://juejin.im/post/5a420adff265da432c241adc
   2.　https://www.jianshu.com/p/831c0114179f
   3.　https://www.jianshu.com/p/beaa56846f50
   4.　https://blog.csdn.net/manypeng/article/details/79475870
4.　如果 Charles 显示连接成功了，这时候在手机上浏览任意页面应该都会有新的数据流被 Charles 截留，显示在 Charles 内。
5.　手机打开到要爬取的公众号的历史文章页，往下滑，注意在电脑上这时会出现对应的链接的信息择。下图中有三个方框，里面的链接之后在扒的时候需要用到。![CharlesScreenshot](assets/CharlesScreenshot-1554280516869.jpg)第一个方框中的内容右键点 copy URL,其他两个右键点 copy content。第一个框中的内容里面有个 offset 字段，这就代表那是你往下划的时候的请求，你要把 offset 等号后面的数字用 {} 替换。这就是我们需要抓取的历史页面下往下滑的时候加载更多数据的那个包。
6.　打开 android_wechat 文件夹下的 python 文件，需要修改三个部分。![placestobeedited](assets/placestobeedited-1554281403895.jpg)其中的 Cookie 和 Referer 直接用上一步中复制的内容就好。下面的那一框则对应上一步中 copu URL得到的东西，直接将内容粘贴上去即可，覆盖掉原本的文本。
7.　在主 python 程序中，即 auto_opt_main.py,修改![1554281773138](assets/1554281773138.png)这三个参数代表程序扒的文章数量和存放的文件夹名字，记得在主文件夹下新建一个 out 文件夹和以 gzhName 命名的文件夹存放 pdf ，否则程序会报错。
8.　运行 auto_opt_main.py 即可，pdf 文件都村到了 /auto_pot-master/out/{gzhName}/ 的文件夹下。





## 调研与尝试：

前期尝试用adb模拟人工操作去一篇一篇获取文章链接并保存到本地，然后通过webdriver打开链接模拟人工按键去用浏览器打印为pdf。这其中还用到了图文识别获取文章标题，中间APP获取并传输链接到PC。虽然最后得到的pdf因为浏览器渲染原因效果很好，但效率很低，爬去一篇文章差不多一分钟，这怎么能忍。后来通过不断学习尝试，得到了用Charles抓包获取文章信息，wkhtmltopdf将网页转换为pdf，虽然wkhtmltopdf有图片无法加载和失真的问题，但都一一解决了。
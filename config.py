# coding:utf-8
'''
定义规则 urls:url列表
         type：解析方式,取值 regular(正则表达式),xpath(xpath解析),module(自定义第三方模块解析)
         patten：可以是正则表达式,可以是xpath语句不过要和上面的相对应
'''
import os
import random

'''
ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https),country(国家),area(省市),updatetime(更新时间)
 speed(连接速度)
'''
parserList = [
    # https://proxy-list.org 国外 需要翻墙
    {
        'urls': ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 21)],
        'type': 'module',
        'moduleName': 'proxy_listPraser',
        'pattern': 'Proxy\(.+\)',
        'position': {'ip': 0, 'port': -1, 'type': -1, 'protocol': 2}
    },


    # http://incloak.com 国外 需要翻墙 能爬到ip，但是感觉ip没一个能用的
    {
        'urls': ['http://incloak.com/proxy-list/%s#list' % n for n in
                 ([''] + ['?start=%s' % (64 * m) for m in range(1, 11)])],
        'useSeleniumDownloader': True,
        'timeout': 30,
        'type': 'xpath',
        'pattern': ".//div[@class='table_block']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # https://ip.ihuan.me 国内 小幻HTTP代理，这个框架暂时无法破解分页
    {
        'urls': [
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5YyX5Lqs.html'  #北京
            'https://ip.ihuan.me/address/5aSp5rSl.html'  #天津
            'https://ip.ihuan.me/address/5LiK5rW3.html'  #上海
            'https://ip.ihuan.me/address/6YeN5bqG.html'  #重庆
            'https://ip.ihuan.me/address/5rKz5YyX.html'  #河北
            'https://ip.ihuan.me/address/5bGx6KW/.html'  #山西
            'https://ip.ihuan.me/address/6L695a6B.html'  #辽宁
            'https://ip.ihuan.me/address/5ZCJ5p6X.html'  #吉林
            'https://ip.ihuan.me/address/6buR6b6Z5rGf.html'  #黑龙江
            'https://ip.ihuan.me/address/5rGf6IuP.html'  #江苏
            'https://ip.ihuan.me/address/5rWZ5rGf.html'  #浙江
            'https://ip.ihuan.me/address/5a6J5b69.html'  #安徽
            'https://ip.ihuan.me/address/56aP5bu6.html'  #福建
            'https://ip.ihuan.me/address/5rGf6KW/.html'  #江西
            'https://ip.ihuan.me/address/5bGx5Lic.html'  #山东
            'https://ip.ihuan.me/address/5rKz5Y2X.html'  #河南
            'https://ip.ihuan.me/address/5rmW5YyX.html'  #湖北
            'https://ip.ihuan.me/address/5rmW5Y2X.html'  #湖南
            'https://ip.ihuan.me/address/5bm/5Lic.html'  #广东
            'https://ip.ihuan.me/address/5rW35Y2X.html'  #海南
            'https://ip.ihuan.me/address/5Zub5bed.html'  #四川
            'https://ip.ihuan.me/address/6LS15bee.html'  #贵州
            'https://ip.ihuan.me/address/5LqR5Y2X.html'  #云南
            'https://ip.ihuan.me/address/6ZmV6KW/.html'  #陕西
            'https://ip.ihuan.me/address/55SY6IKD.html'  #甘肃
            'https://ip.ihuan.me/address/6Z2S5rW3.html'  #青海
            'https://ip.ihuan.me/address/5Y+w5rm+.html'  #台湾
            'https://ip.ihuan.me/address/5YaF6JKZ5Y+k.html'  #内蒙古
            'https://ip.ihuan.me/address/5bm/6KW/.html'  #广西
            'https://ip.ihuan.me/address/6KW/6JeP.html'  #西藏
            'https://ip.ihuan.me/address/5a6B5aSP.html'  #宁夏
            'https://ip.ihuan.me/address/5paw55aG.html'  #新疆
            'https://ip.ihuan.me/address/6aaZ5riv.html'  #香港
            'https://ip.ihuan.me/address/576O5Zu9.html'  #美国
            'https://ip.ihuan.me/address/5oSP5aSn5Yip.html'  #意大利
            'https://ip.ihuan.me/address/5Lym5be056ys5aSn5Yy6.html'  #伦巴第大区
            'https://ip.ihuan.me/address/57Gz5YWw5bm/5Z+f5biC.html'  #米兰广域市
            'https://ip.ihuan.me/address/5Y2w5bqm.html'  #印度
            'https://ip.ihuan.me/address/5Y2h57qz5aGU5YWL6YKm.html'  #卡纳塔克邦
            'https://ip.ihuan.me/address/54+t5Yqg572X5bCU.html'  #班加罗尔
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5YyX5Lqs.html'  #北京
            'https://ip.ihuan.me/address/5Y2w5bqm5bC86KW/5Lqa.html'  #印度尼西亚
            'https://ip.ihuan.me/address/5Lit5Yqg6YeM5pu85Li555yB.html'  #中加里曼丹省
            'https://ip.ihuan.me/address/5biV5pyX5Y2h5ouJ5Lqa5biC.html'  #帕朗卡拉亚市
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5bm/5Lic.html'  #广东
            'https://ip.ihuan.me/address/5rex5Zyz.html'  #深圳
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5rGf6IuP.html'  #江苏
            'https://ip.ihuan.me/address/5Y2X6YCa.html'  #南通
            'https://ip.ihuan.me/address/6Z+p5Zu9.html'  #韩国
            'https://ip.ihuan.me/address/6aaW5bCU.html'  #首尔
            'https://ip.ihuan.me/address/5L+E572X5pav.html'  #俄罗斯
            'https://ip.ihuan.me/address/6L2m6YeM6ZuF5a6+5pav5YWL5bee.html'  #车里雅宾斯克州
            'https://ip.ihuan.me/address/6L2m6YeM6ZuF5a6+5pav5YWL.html'  #车里雅宾斯克
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5YyX5Lqs.html'  #北京
            'https://ip.ihuan.me/address/5Z2m5qGR5bC85Lqa.html'  #坦桑尼亚
            'https://ip.ihuan.me/address/5aSa5aSa6ams5Yy6.html'  #多多马区
            'https://ip.ihuan.me/address/5aSa5aSa6ams.html'  #多多马
            'https://ip.ihuan.me/address/5qC86bKB5ZCJ5Lqa.html'  #格鲁吉亚
            'https://ip.ihuan.me/address/5Z2m5qGR5bC85Lqa.html'  #坦桑尼亚
            'https://ip.ihuan.me/address/5aSa5aSa6ams5Yy6.html'  #多多马区
            'https://ip.ihuan.me/address/5aSa5aSa6ams.html'  #多多马
            'https://ip.ihuan.me/address/5qC86bKB5ZCJ5Lqa.html'  #格鲁吉亚
            'https://ip.ihuan.me/address/5aGe5YaF5Yqg5bCU.html'  #塞内加尔
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5rKz5Y2X.html'  #河南
            'https://ip.ihuan.me/address/6YOR5bee.html'  #郑州
            'https://ip.ihuan.me/address/576O5Zu9.html'  #美国
            'https://ip.ihuan.me/address/5byX5ZCJ5bC85Lqa5bee.html'  #弗吉尼亚州
            'https://ip.ihuan.me/address/5pav54m554G1.html'  #斯特灵
            'https://ip.ihuan.me/address/5LmM5YW55Yir5YWL5pav5Z2m.html'  #乌兹别克斯坦
            'https://ip.ihuan.me/address/5aGU5LuA5bmy.html'  #塔什干
            'https://ip.ihuan.me/address/5Lit5Zu9.html'  #中国
            'https://ip.ihuan.me/address/5bm/5Lic.html'  #广东
            'https://ip.ihuan.me/address/5rGV5aS0.html'  #汕头
        ],
        'useSeleniumDownloader': True,
        'type': 'xpath',
        'pattern': ".//div[@class='table-responsive']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # https://www.89ip.cn 国内 89ip
    {
        'urls': ['https://www.89ip.cn/index_%s.html' % n for n in range(1, 21)],
        'type': 'xpath',
        'pattern': ".//div[@class='layui-form']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # https://www.beesproxy.com 国内 蜜蜂代理
    {
        'urls': ['https://www.beesproxy.com/free/page/%s' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//figure[@class='wp-block-table']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # http://www.kxdaili.com 国内 开心代理
    {
        'urls': ['http://www.kxdaili.com/dailiip/1/%s.html' % n for n in range(1, 11)] + ['http://www.kxdaili.com/dailiip/2/%s.html' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//figure[@class='wp-block-table']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    #https://www.kgtools.cn 国内 KGtools
    {
        'urls': ['https://www.kgtools.cn/api/proxy/ops/list/?label=1&name=全国代理ip&page=%s' % n for n in range(1, 21)],
        'type': 'regular',
        'pattern':  r'"proxy_ip":\s*"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",\s*"port":\s*"(\d+)"',
        'position': {'ip': 0, 'port': 1, 'type': '', 'protocol': ''}
    },

    # https://www.89ip.cn 国内 69免费代理
    {
        'urls': ['https://www.69ip.cn/?page=%s' % n for n in range(1, 5)],
        'type': 'xpath',
        'pattern': ".//div[@class='layui-form']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # https://proxy.ip3366.net 国内 齐云代理
    {
        'urls': ['https://proxy.ip3366.net/free/?action=china&page=%s' % n for n in range(1, 11)],
        'type': 'xpath',
        'pattern': ".//table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # https://www.docip.net/ 国内 稻壳代理
    {
        'urls': ['https://www.docip.net/data/free.json'],
        'type': 'regular',
        'pattern':  r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)',
        'position': {'ip': 0, 'port': 1, 'type': '', 'protocol': ''}
    },

    # https://www.kuaidaili.com/ 国内 快代理
    {
        'urls': [
            'https://www.kuaidaili.com/free/dps/',
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ],
        'type': 'xpath',
        'pattern': ".//table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },

    # http://free-proxy.cz/ 国外 新鲜代理 需要翻墙
    {
        'urls':
            ['http://free-proxy.cz/zh/proxylist/country/CN/https/ping/level1/%s' % n for n in range(1, 6)]  # 中国HTTPS
            + ['http://free-proxy.cz/zh/proxylist/country/CN/http/ping/level1/%s' % n for n in range(1, 6)]  # 中国HTTP
            + ['http://free-proxy.cz/zh/proxylist/country/all/https/ping/level1/%s' % n for n in range(1, 6)]  # 全部HTTPS
            + ['http://free-proxy.cz/zh/proxylist/country/all/http/ping/level1/%s' % n for n in range(1, 6)]  # 全部HTTP
        ,
        'type': 'xpath',
        'pattern': ".//div[@class='layui-form']/table/tbody/tr",
        'position': {'ip': './td[1]', 'port': './td[2]', 'type': '', 'protocol': ''}
    },
]
'''
数据库的配置
'''
DB_CONFIG = {

    'DB_CONNECT_TYPE': 'sqlalchemy',  # 'pymongo'sqlalchemy;redis
    # 'DB_CONNECT_STRING':'mongodb://localhost:27017/'
    # 'DB_CONNECT_STRING': 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'
    'DB_CONNECT_STRING': 'mysql+pymysql://ip_proxy_pool:pTCeejECSFzya7y3@192.168.1.5/ip_proxy_pool?charset=utf8'

    # 'DB_CONNECT_TYPE': 'redis',  # 'pymongo'sqlalchemy;redis
    # 'DB_CONNECT_STRING': 'redis://localhost:6379/8',

}
CHINA_AREA = ['河北', '山东', '辽宁', '黑龙江', '吉林'
    , '甘肃', '青海', '河南', '江苏', '湖北', '湖南',
              '江西', '浙江', '广东', '云南', '福建',
              '台湾', '海南', '山西', '四川', '陕西',
              '贵州', '安徽', '重庆', '北京', '上海', '天津', '广西', '内蒙', '西藏', '新疆', '宁夏', '香港', '澳门']
QQWRY_PATH = os.path.dirname(__file__) + "/data/qqwry.dat"
THREADNUM = 5
API_PORT = 8000
'''
爬虫爬取和检测ip的设置条件
不需要检测ip是否已经存在，因为会定时清理
'''
UPDATE_TIME = 10 * 60  # 多久检测一次是否有代理ip失效(秒) 默认值：30*60
MINNUM = 50  # 当有效的ip值小于一个时 需要启动爬虫进行爬取

TIMEOUT = 10  # socket延时
'''
反爬虫的设置
'''
'''
重试次数
'''
RETRY_TIME = 3

'''
USER_AGENTS 随机头信息
'''
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]


def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
#默认给抓取的ip分配20分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
DEFAULT_SCORE=10

TEST_URL = 'http://ip.chinaz.com/getip.aspx'
TEST_IP = 'http://httpbin.org/ip'
TEST_HTTP_HEADER = 'http://httpbin.org/get'
TEST_HTTPS_HEADER = 'https://httpbin.org/get'
#CHECK_PROXY变量是为了用户自定义检测代理的函数
#现在使用检测的网址是httpbin.org,但是即使ip通过了验证和检测
#也只能说明通过此代理ip可以到达httpbin.org,但是不一定能到达用户爬取的网址
#因此在这个地方用户可以自己添加检测函数,我以百度为访问网址尝试一下
#大家可以看一下Validator.py文件中的baidu_check函数和detect_proxy函数就会明白

CHECK_PROXY={'function':'checkProxy'}#{'function':'baidu_check'}

#下面配置squid,现在还没实现
#SQUID={'path':None,'confpath':'C:/squid/etc/squid.conf'}

MAX_CHECK_PROCESS = 2 # CHECK_PROXY最大进程数 默认值：2
MAX_CHECK_CONCURRENT_PER_PROCESS = 10 # CHECK_PROXY时每个进程的最大并发 默认值: 30 PS：，这里是个坑没达到数量就不验证IP
TASK_QUEUE_SIZE = 50 # 任务队列SIZE
MAX_DOWNLOAD_CONCURRENT = 3 # 从免费代理网站下载时的最大并发 
CHECK_WATI_TIME = 1 #进程数达到上限时的等待时间
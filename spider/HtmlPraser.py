# coding:utf-8
import base64
import sys
import traceback
from config import QQWRY_PATH, CHINA_AREA
from util.IPAddress import IPAddresss
import re
from util.compatibility import text_

__author__ = 'qiye'
from lxml import etree


class Html_Parser(object):
    def __init__(self):
        self.ips = IPAddresss(QQWRY_PATH)

    def parse(self, url, response, parser):
        '''

        :param url:
        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        if parser['type'] == 'xpath':
            return self.XpathPraser(url, response, parser)
        elif parser['type'] == 'regular':
            return self.RegularPraser(url, response, parser)
        elif parser['type'] == 'module':
            return getattr(self, parser['moduleName'], None)(url, response, parser)
        else:
            return None

    def AuthCountry(self, addr):
        '''
        用来判断地址是哪个国家的
        :param addr:
        :return:
        '''
        for area in CHINA_AREA:
            if text_(area) in addr:
                return True
        return False

    def XpathPraser(self, url, response, parser):
        '''
        针对xpath方式进行解析
        :param url:
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = proxy.xpath(parser['position']['port'])[0].text
                if ip is None:
                    ip = proxy.xpath(f"string({parser['position']['ip']})")
                if port is None:
                    port = proxy.xpath(f"string({parser['position']['port']})")
                ip = ip.strip()
                port = port.strip()
                types = 0
                protocol = 0
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                country = text_('')
                area = text_('')
                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr
            except Exception as e:
                log = f'IPProxyPool----->>>>>>>> {url} 解析IP失败: [{type(e).__module__}.{type(e).__name__}]{e}'
                log += f'\r\n{traceback.format_exc()}'
                sys.stdout.write(log + "\r\n")
                sys.stdout.flush()
                continue
            # updatetime = datetime.datetime.now()
            # ip，端口，类型(0高匿名，1透明)，protocol(0 http,1 https http),country(国家),area(省市),updatetime(更新时间)

            # proxy ={'ip':ip,'port':int(port),'type':int(type),'protocol':int(protocol),'country':country,'area':area,'updatetime':updatetime,'speed':100}
            proxy = {'ip': ip, 'port': int(port), 'types': int(types), 'protocol': int(protocol), 'country': country,
                     'area': area, 'speed': 100}
            proxylist.append(proxy)
        return proxylist

    def RegularPraser(self, url, response, parser):
        '''
        针对正则表达式进行解析
        :param url:
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        if matchs != None:
            for match in matchs:
                try:
                    ip = match[parser['position']['ip']]
                    port = match[parser['position']['port']]
                    # 网站的类型一直不靠谱所以还是默认，之后会检测
                    type = 0
                    # if parser['postion']['protocol'] > 0:
                    # protocol = match[parser['postion']['protocol']]
                    # if protocol.lower().find('https')!=-1:
                    #         protocol = 1
                    #     else:
                    #         protocol = 0
                    # else:
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    # print(ip,port)
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    continue

                proxy = {'ip': ip, 'port': port, 'types': type, 'protocol': protocol, 'country': country, 'area': area,
                         'speed': 100}

                proxylist.append(proxy)
            return proxylist

    def CnproxyPraser(self, url, response, parser):
        proxylist = self.RegularPraser(url, response, parser)
        chardict = {'v': '3', 'm': '4', 'a': '2', 'l': '9', 'q': '0', 'b': '5', 'i': '7', 'w': '6', 'r': '8', 'c': '1'}

        for proxy in proxylist:
            port = proxy['port']
            new_port = ''
            for i in range(len(port)):
                if port[i] != '+':
                    new_port += chardict[port[i]]
            new_port = int(new_port)
            proxy['port'] = new_port
        return proxylist

    def proxy_listPraser(self, url, response, parser):
        proxylist = []
        pattern = re.compile(parser['pattern'])
        try:
            matchs = pattern.findall(response)
        except Exception as e:
            log = f'IPProxyPool----->>>>>>>> {url} 解析IP失败: [{type(e).__module__}.{type(e).__name__}]{e}'
            log += f'\r\n{traceback.format_exc()}'
            sys.stdout.write(log + "\r\n")
            sys.stdout.flush()
            return proxylist
        if matchs:
            for match in matchs:
                try:
                    ip_port = base64.b64decode(match.replace("Proxy('", "").replace("')", ""))
                    if type(ip_port) == bytes:
                        ip_port = ip_port.decode('utf-8')
                    ip = ip_port.split(':')[0]
                    port = ip_port.split(':')[1]
                    types = 0
                    protocol = 0
                    addr = self.ips.getIpAddr(self.ips.str2ip(ip))
                    country = text_('')
                    area = text_('')
                    # print(ip,port)
                    if text_('省') in addr or self.AuthCountry(addr):
                        country = text_('国内')
                        area = addr
                    else:
                        country = text_('国外')
                        area = addr
                except Exception as e:
                    log = f'IPProxyPool----->>>>>>>> {url} 解析IP失败: [{type(e).__module__}.{type(e).__name__}]{e}'
                    log += f'\r\n{traceback.format_exc()}'
                    sys.stdout.write(log + "\r\n")
                    sys.stdout.flush()
                    continue
                proxy = {'ip': ip, 'port': int(port), 'types': types, 'protocol': protocol, 'country': country,
                         'area': area, 'speed': 100}
                proxylist.append(proxy)
            return proxylist








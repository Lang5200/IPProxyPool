# coding:utf-8

import random
import sys

import undetected_chromedriver as uc

import config
from db.DataStore import sqlhelper

__author__ = 'qiye'

import requests
import chardet


class Html_Downloader(object):
    @staticmethod
    def download(url, parser, request_times=-1):
        """
        :param url:
        :param parser:
        :param proxy:
        :param request_times: 已请求次数
        :return: 失败为False
        """
        request_times += 1

        timeout = config.TIMEOUT
        if 'timeout' in parser:
            timeout = parser['timeout']

        proxy = None
        if request_times > 0:
            proxylist = sqlhelper.select(10)
            if not proxylist:
                log = f'IPProxyPool----->>>>>>>> {url} 下载失败（{request_times}）: 无可用的代理IP！'
                sys.stdout.write(log + "\r\n")
                sys.stdout.flush()
                return False

            proxy = random.choice(proxylist)

        driver = None
        try:
            if 'useSeleniumDownloader' in parser and parser['useSeleniumDownloader']:
                options = uc.ChromeOptions()
                # 禁用图片和CSS, 提升速度
                prefs = {
                    "profile.managed_default_content_settings.images": 2,
                    "permissions.default.stylesheet": 2,
                }
                options.add_experimental_option("prefs", prefs)
                # 屏蔽控制台报错 & 设置日志级别
                options.add_argument('--log-level=3')  # 可能的值包括: 3 (错误), 2 (警告), 1 (信息), 0 (调试)
                # 设置Header
                for key, value in config.get_header().items():
                    options.add_argument(f"--{key}={value}")
                # 设置代理
                if proxy is not None:
                    options.add_argument(f'--proxy-server={proxy[0]}:{proxy[1]}')

                driver = uc.Chrome(headless=True, use_subprocess=False, options=options)

                driver.get(url)
                driver.implicitly_wait(timeout)
                content = driver.page_source
                driver.quit()

                if len(content) < 500:
                    raise ConnectionError
            else:
                proxies = None
                if proxy is not None:
                    proxies = {"http": f"http://{proxy[0]}:{proxy[1]}", "https": f"http://{proxy[0]}:{proxy[1]}"}
                r = requests.get(url=url, headers=config.get_header(), timeout=timeout, proxies=proxies)
                r.encoding = chardet.detect(r.content)['encoding']
                if (not r.ok) or len(r.content) < 500:
                    raise ConnectionError
                content = r.text

            if "性能和安全由" in str(content) and "Cloudflare" in str(content):
                raise ConnectionError("触发Cloudflare！")

            return content
        except Exception as e:
            if driver is not None:
                driver.quit()
                pass

            log = (f"IPProxyPool----->>>>>>>> {url} proxy:{f'({proxy[0]}:{proxy[1]})' if proxy is not None else ''} 下载失败{f'（{request_times}）' if request_times > 0 else ''}: "
                   f"[{type(e).__module__}.{type(e).__name__}]{e}")
            # 很多异常都非常长，谨慎操作...
            # skip = False
            # if isinstance(e, WebDriverException):  # 这个异常视乎非常长 跳过
            #     skip = True
            #
            # if not skip:
            #     error_info = "    " + traceback.format_exc().replace("\n", "\n    ")
            #     log += f"\r\n{error_info}"
            sys.stdout.write(log + "\r\n")
            sys.stdout.flush()

            if request_times >= config.RETRY_TIME:
                log = f"IPProxyPool----->>>>>>>> {url} proxy:{f'({proxy[0]}:{proxy[1]})' if proxy is not None else ''} 下载失败（{request_times}）: 已达到最大重试次数！"
                sys.stdout.write(log + "\r\n")
                sys.stdout.flush()
                return False
            else:
                return Html_Downloader.download(url, parser, request_times)

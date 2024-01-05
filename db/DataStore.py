# coding:utf-8
import sys
import traceback

from config import DB_CONFIG
from util.exception import Con_DB_Fail


try:
    if DB_CONFIG['DB_CONNECT_TYPE'] == 'pymongo':
        from db.MongoHelper import MongoHelper as SqlHelper
    elif DB_CONFIG['DB_CONNECT_TYPE'] == 'redis':
        from db.RedisHelper import RedisHelper as SqlHelper
    else:
        from db.SqlHelper import SqlHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
except Exception as e:
    raise Con_DB_Fail


def store_data(queue2, db_proxy_num):
    '''
    读取队列中的数据，写入数据库中
    :param queue2:
    :return:
    '''
    successNum = 0
    failNum = 0
    while True:
        try:
            proxy = queue2.get(timeout=300)
            if proxy:
                sqlhelper.insert(proxy)
                successNum += 1
            else:
                failNum += 1
            ip = f"新的IP（{proxy['ip']}:{proxy['port']}） " if proxy is not None else ''
            log = f"IPProxyPool----->>>>>>>> {ip}总计IP：{successNum+failNum} 成功IP：{successNum}，失败IP：{failNum}"
            # 这里容易失效，改print
            # sys.stdout.write(log + "\r")
            # sys.stdout.flush()
            print(log)
        except BaseException as e:
            log = (
                f"IPProxyPool----->>>>>>>> 储存异常: "
                f"[{type(e).__module__}.{type(e).__name__}]{e}")
            error_info = "    " + traceback.format_exc().replace("\n", "\n    ")
            log += f"\r\n{error_info}"
            sys.stdout.write(log + "\r\n")
            sys.stdout.flush()
            if db_proxy_num.value != 0:
                successNum += db_proxy_num.value
                db_proxy_num.value = 0
                log = f'IPProxyPool----->>>>>>>> 总计IP：{successNum+failNum} 成功IP：{successNum}，失败IP：{failNum}'
                # 这里容易失效，改print
                # sys.stdout.write(log + "\r")
                # sys.stdout.flush()
                print(log)
                successNum = 0
                failNum = 0



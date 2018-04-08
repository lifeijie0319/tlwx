#-*- coding:utf-8 -*-
import json
import redis
import requests
import time

from app.config import ACCESS_TOKEN_KEY, JSAPI_TICKET_KEY, REDIS
from app.service.wx import weixin_access_token


redis_conn = redis.StrictRedis(host=REDIS.get('HOST'), port=REDIS.get('PORT'), db=0)


def update_access_token():
    #logger.debug('accessing the access_token')
    access_token, expires_in = weixin_access_token()
    print(time.strftime('%Y-%m-%d %H:%m:%S',time.localtime()), '\n', redis_conn.get(ACCESS_TOKEN_KEY))
    if access_token:
        #logger.debug('%s, %s', access_token, expires_in)
        url='https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        params={'access_token': access_token, 'type': 'jsapi'}
        res=requests.get(url, params)
        redis_conn.set(JSAPI_TICKET_KEY, res.json().get('ticket'))
    else:
        count = 0
        while not access_token and count < 3:
            time.sleep(60)
            access_token, expires_in = weixin_access_token()
            #logger.debug('这是第%d次重新获取access_token' %(count + 1))
            count += 1
        if count == 3:
            #logger.debug("多次获取access_token失败，请排查错误")
            exit()
    print('ACCESS_TOKEN', access_token)
    redis_conn.set(ACCESS_TOKEN_KEY, access_token)


if __name__ == '__main__':
    update_access_token()

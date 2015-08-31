#!/usr/bin/env python

import sys,os
import ConfigParser
import json
import requests

conf = 'wxAlert.conf'

config = ConfigParser.ConfigParser()
config.read(conf)

wxappid         = config.get('default', 'appid')
wxsecret        = config.get('default', 'secret')
template_id     = config.get('default', 'template_id')


gettokenuri="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(wxappid,wxsecret)

get_token = requests.get(gettokenuri)
get_token=json.loads(get_token.text)
token=get_token['access_token']


getuseruri="https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s"%(token)

get_user = requests.get(getuseruri)
get_user = json.loads(get_user.text)
openids  = get_user['data']['openid']

for openid in openids:
    userinfouri="https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s"%(token,openid)
    user_info = requests.get(userinfouri)
    user_info = json.loads(user_info.text)
    print 'nickname: ',   user_info['nickname']
    print 'openid: ',     user_info['openid']
    print 'headimgurl: ', user_info['headimgurl']

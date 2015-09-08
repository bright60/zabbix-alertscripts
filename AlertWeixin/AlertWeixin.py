#!/usr/bin/env python

import sys,os
import ConfigParser
import json
import requests

conf = './AlertWeixin.conf'

config = ConfigParser.ConfigParser()
config.read(conf)

wxappid         = config.get('default', 'appid')
wxsecret        = config.get('default', 'secret')
template_id     = config.get('default', 'template_id')


useropenid  = sys.argv[1]
touser      = useropenid
first       = sys.argv[2]
keyword1    = sys.argv[3]
keyword2    = sys.argv[4]
keyword3    = sys.argv[5]
remark      = sys.argv[6]


gettokenuri="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(wxappid,wxsecret)

get_token = requests.get(gettokenuri)
get_token=json.loads(get_token.text)
token=get_token['access_token']


payload='{\n\
"touser":"%s",\n\
"template_id":"%s",\n\
"url":"http://weixin.qq.com/download",\n\
"topcolor":"#FF0000",\n\
"data":{\n\
"first": {\n\
"value":"%s",\n\
"color":"#173177"\n\
},\n\
"keyword1":{\n\
"value":"%s",\n\
"color":"#173177"\n\
},\n\
"keyword2":{\n\
"value":"%s",\n\
"color":"#173177"\n\
},\n\
"keyword3":{\n\
"value":"%s",\n\
"color":"#173177"\n\
},\n\
"remark":{\n\
"value":"%s",\n\
"color":"#173177"\n\
}\n\
}\n\
}'%(touser,template_id,first,keyword1,keyword2,keyword3,remark)


alteruri="https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"%(token)

AlertWeixin = requests.post(alteruri, data=payload)

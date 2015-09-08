#!/usr/bin/env python
#coding=utf-8

#-*- coding: UTF-8 -*-

from CCPRestSDK import REST
from yuntongxun import *

def voiceVerify(to,verifyCode):

    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)

    playTimes	= 2
    respUrl	= ''
    lang	= ''
    userData	= ''

    result = rest.voiceVerify(verifyCode,playTimes,to,displayNum,respUrl,lang,userData)
    for k,v in result.iteritems():

        if k=='VoiceVerify' :
                for k,s in v.iteritems():
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)

vTo=sys.argv[1]
vCode=sys.argv[2]

voiceVerify(vTo,vCode)


#!/usr/bin/env python
#coding=utf-8

#-*- coding: UTF-8 -*-

from CCPRestSDK import REST
from yuntongxun import *

def landingCall(to):

    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)

    mediaTxt    = ''
    playTimes   = 2
    respUrl     = ''
    userData    = ''
    maxCallTime = ''
    speed       = ''
    volume      = ''
    pitch       = ''
    bgsound     = ''

    result = rest.landingCall(to,mediaName,mediaTxt,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound)
    for k,v in result.iteritems():

        if k=='LandingCall' :
                for k,s in v.iteritems():
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)



lTo=sys.argv[1]
landingCall(lTo)

#!/usr/bin/env python
#coding=utf-8

#-*- coding: UTF-8 -*-


import sys,os
import ConfigParser

conf = 'yuntongxun.conf'

config = ConfigParser.ConfigParser()
config.read(conf)

#主帐号
accountSid      = config.get('default', 'accountSid')

#主帐号Token
accountToken    = config.get('default', 'accountToken')

#应用Id
appId           = config.get('default', 'appId')

#请求地址
serverIP        = config.get('default', 'serverIP')

#请求端口
serverPort='8883';

#REST版本号
softVersion='2013-12-26';


mediaName       = config.get('default', 'mediaName')
displayNum      = config.get('default', 'displayNum')


# ZABBIX告警电话通知
虽然我们已经有配置了多种告警通知方式（邮件，短信， [微信](https://github.com/vincihu/misc/tree/master/AlertWeixin) ），但是对于没有配备24小时值班岗位的运维团队来说，还是会有一个困扰，在夜深人静夜黑风高，运维同学睡着后，如何进行有效的告警通知。

在思考这个问题的时候，就需要启用告警电话通知了。

有告警电话帮助，运维同学再也不用在业务处理异常，触发的常规告警通知未叫醒自己而导致故障升级一直到事件“惊醒”到leader、主管、CEO，再打电话叫醒睡梦中自己，然后迷迷糊糊被骂一顿继续处理故障。在故障发生、触发告警电话通知的第一时间，就可以进行事件介入和故障恢复。

下面介绍我使用进行告警电话通知的配置方法

---
### 本处介绍的电话通知，使用了[云通讯](http://www.yuntongxun.com/)的服务，有两种通知方式:

1. 电话播报语音验证码
	- 配置最简单
	- 呼叫费用(0.06元/次)，没有其他成本
	- 电话接听后播报语音验证码，可能会造成困惑
2. 电话播报预录制语音
	- 配置简单
	- 呼叫费用(0.06元/次)
    - 需要启用IVR功能
   		- 费用100元/月
	- 可以预先录制告警语音
		- 可根据业务/项目，录制不同的语音内容
	- 可使用TTS功能，语音播报告警内容
		- 费用200元/月



---

## 一、注册云通讯账号，并进行企业账号认证
[荣联·云通讯](http://www.yuntongxun.com/)

## 二、创建应用
- 记录下账号ID以及应用的APP ID/TOKEN，备用
- 如果使用“电话播报预录制语音”的方式，需要在控制台额外配置
	- 启用IVR功能
	- 上传预录制的语音 alertnotify.wav
		- 可找妹纸录制，或者使用TTS软件生成
		- 在[控制台-管理-应用列表-应用详情-语音库管理]页面上传

## 三、下载配置告警通知脚本

```
# 下载告警通知脚本
$ git clone https://github.com/vincihu/misc/
# 部署告警通知脚本到zabbix的alertscripts目录
$ sudo mv misc/AlertCall /usr/lib/zabbix/alertscripts/
$ sudo ln -s /usr/lib/zabbix/alertscripts/{AlertCall/AlertCall.sh,}
$ sudo mkdir /usr/lib/zabbix/alertscripts/logs
# 为脚本添加zabbix用户执行权限
$ sudo chmod u+x AlertCall.sh
$ sudo chown zabbix:zabbix /usr/lib/zabbix/alertscripts/{logs/,AlertCall.sh}
# 安装需要的python模块
$ sudo pip install -U configparser
# 初始化环境
$ sudo mkdir /var/run/zabbix/AlertCall/
$ sudo chown zabbix:zabbix /var/run/zabbix/AlertCall/
```
修改AlertCall/yuntongxun.conf，填入账号相关信息

```
[default]
accountSid      = {accountSid}
accountToken    = {accountToken}
appId           = {appId}
```

- 告警通知脚本默认使用“电话播报预录制语音”方式，如果使用“电话播报语音验证码”方式，需要修改AlertCall.sh尾部的内容（两处修改）

	```
#VoiceVerify $PNUM
LandingCall $PNUM
```
	修改为
	
	```
VoiceVerify $PNUM
#LandingCall $PNUM
```

## 四、测试脚本

```
$ cd /usr/lib/zabbix/alertscripts/
$ sudo -u zabbix bash AlertCall.sh {your mobile number}
```


## 五、配置Zabbix

1. 添加Media type(告警媒介)

	```
Name:			X. AlertCall
Type:			Script
Script name:	AlertCall.sh
```

2. 配置profile - Media(告警接收ID)

	```
Type:			X. AlertCall
Send to:		{Mobile}
```

## 六、测试验证
模拟触发告警，验证告警电话通知功能
	
---
## 其他 -

### 海外使用云通讯的网络问题
因为云通讯服务器在阿里云杭州，而阿里云杭州的国际链路质量非常非常差，如果你的监控服务器在海外的话，可能会出现呼叫请求网络错误的情况（脚本里已有遇到网络错误时重试的逻辑），那么就需要用到代理做访问云通讯API的加速

1. 在海外监控服务器和阿里云杭州之间，找寻网络质量比较稳定的节点
	- 推荐使用香港节点
	- 其他国内服务器也可
2. 配置代理服务
	1. HTTPS代理
		- tinyproxy
		- 3proxy
	2. TCP代理
		- nginx (version>=1.9.0)
		- haproxy
	3. iptables端口转发
	
		```
		iptables -t nat -A PREROUTING -s {monitor.ip.addr.ess}/32 -d {proxy.ip.addr.ess}/32 -p tcp -m tcp --dport 8883 -j DNAT --to-destination 42.121.254.126:8883
iptables -t nat -A POSTROUTING -d 42.121.254.126/32 -p tcp -m tcp -j MASQUERADE
		```
3. 在海外监控服务器配置HOSTS

	```
	{monitor.ip.addr.ess}   app.cloopen.com
	```



### 其他语音呼叫功能提供商

- [nexmo](https://www.nexmo.com/)
	- 语音呼叫 价格 €0.0120/min
		- 按秒计费，单次呼叫成本会比云通讯更低
	- 固定号码 价格 €19.00/month


### 扩展阅读
有意向开发自己的语音告警平台的同学，可以参考另一位大侠做的[《zabbix企业应用之自动语音报警平台》](
http://dl528888.blog.51cto.com/2382721/1639579)

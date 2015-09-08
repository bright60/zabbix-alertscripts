#!/bin/bash

test "$#" -lt 1 && exit 1

PNUM=$1
echo $PNUM |egrep -c -w '1[0-9]{10}' >/dev/null || exit 1

function VoiceVerify () {
  PNUM=$1
  TIMESTAMP=$(date +%s)
  VCODE=${TIMESTAMP: -4}
  LOG=/usr/lib/zabbix/alertscripts/logs/VoiceVerify.log

  cd /usr/lib/zabbix/alertscripts/AlertCall/
  echo start : `date +%F" "%T` "============="      >> $LOG
  python VoiceVerify.py $PNUM $VCODE  >> $LOG  2>&1
  echo end   : `date +%F" "%T` "============="      >> $LOG
  echo                                              >> $LOG
}

function LandingCall () {
  PNUM=$1
  LOG=/usr/lib/zabbix/alertscripts/logs/LandingCall.log

  cd /usr/lib/zabbix/alertscripts/AlertCall/
  echo start : `date +%F" "%T` "============="      >> $LOG
  python LandingCall.py $PNUM         >> $LOG  2>&1
  echo end   : `date +%F" "%T` "============="      >> $LOG
  echo                                              >> $LOG
}

# 初始化环境
mkdir -p /var/run/zabbix/AlertCall/
cd /var/run/zabbix/AlertCall/
touch calling.$PNUM.timestamp


#0. sleep 0-9 s
sleep "${RANDOM: -1}"

#1. 判断距离上次呼叫是否间隔500s,如果小于则直接退出
CSTAMP=$(cat calling.$PNUM.timestamp)
if [ -n "$CSTAMP" ]
then
  OTIME=$(echo `date +%s` - $CSTAMP|bc)
  test $OTIME -lt 500 && exit 3
fi

#2. 更新最近一次呼叫发出的时间戳
date +%s   > calling.$PNUM.timestamp

#3. 呼叫
#while ! ( nc -w2 app.cloopen.com 8883 )
#do
#  sleep 7
#done

#VoiceVerify $PNUM
LandingCall $PNUM

#4. 如果网络问题呼叫失败,重试
LOG=/usr/lib/zabbix/alertscripts/logs/LandingCall.log
while (grep -A4 $PNUM $LOG |tail -1|grep 172001 >/dev/null 2>&1)
do
  sleep 15
  #VoiceVerify $PNUM
  LandingCall $PNUM
  date +%s   > calling.$PNUM.timestamp
done


exit 0

#!/bin/bash

user="$1"
subject="$2"
content="$3"

useropenid=$user
eventtime=$(echo "$content" |grep "Event tim" |sed -e 's#.$##' -e 's#Event time: ## ' )
itemvalue=$(echo "$content" |tail -3 |head -1 |sed -e 's#.$##' -e 's#1. ##' )

touser=$useropenid
first="$subject"
keyword1=""
keyword2=$eventtime
keyword3=$itemvalue
remark=""



cd /usr/lib/zabbix/alertscripts/AlertWeixin/

python ./AlertWeixin.py "$touser" "$first" "$keyword1" "$keyword2" "$keyword3" "$remark" 2>&1 |\
  grep -i -v insecureplatformwarning >> ../logs/AlertWeixin.log 

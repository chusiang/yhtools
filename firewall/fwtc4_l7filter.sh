#!/bin/bash
#本 shell 僅供參考，無法直接執行
LANG="zh_TW.UTF-8"
PATH="/sbin:/usr/sbin:/bin:/usr/bin"

iptables -F
iptables -t nat -F
iptables -t mangle -F

tc qdisc del dev eth1 root 2> /dev/unll
tc qdisc del dev eth2 root 2> /dev/unll
#定義上下載限速
UP_TOTAL="100"
UP_P2P="40"
UP_OTHER="60"

DOWN_TOTAL="100"
DOWN_P2P="30"
DOWN_OTHER="70"
#定義上傳之流量eth1
tc qdisc add dev eth1 root handle 1: htb default 20
tc class add dev eth1 parent 1: classid 1:1 htb rate "$UP_TOTAL"kbps ceil "$UP_TOTAL"kbps
tc class add dev eth1 parent 1:1 classid 1:10 htb rate "$UP_P2P"kbps ceil "$UP_P2P"kbps
tc class add dev eth1 parent 1:1 classid 1:20 htb rate "$UP_OTHER"kbps ceil "$UP_OTHER"kbps
tc qdisc add dev eth1 parent 1:10 handle 11: pfifo
tc qdisc add dev eth1 parent 1:20 handle 12: pfifo
tc filter add dev eth1 parent 1: protocol ip handle 100 fw classid 1:10
#定義下載之流量eth2

tc qdisc add dev eth2 root handle 2: htb default 20
tc class add dev eth2 parent 2: classid 2:1 htb rate "$DOWN_TOTAL"kbps ceil "$DOWN_TOTAL"kbps
tc class add dev eth2 parent 2:1 classid 2:10 htb rate "$DOWN_P2P"kbps ceil "$DOWN_P2P"kbps
tc class add dev eth2 parent 2:1 classid 2:20 htb rate "$DOWN_OTHER"kbps ceil "$DOWN_OTHER"kbps
tc qdisc add dev eth2 parent 2:10 handle 21: pfifo
tc qdisc add dev eth2 parent 2:20 handle 22: pfifo
tc filter add dev eth2 parent 2: protocol ip handle 200 fw classid 2:10

for proto in edonkey bittorrent ares fasttrack gnutella
do
#下載
iptables -t mangle -A FORWARD -m layer7 --l7proto $proto -m physdev --physdev-in eth1 --physdev-out eth2 -j MARK --set-mark 200
#上傳
iptables -t mangle -A FORWARD -m layer7 --l7proto $proto -m physdev --physdev-in eth2 --physdev-out eth1 -j MARK --set-mark 100
done 

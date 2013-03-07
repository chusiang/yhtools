#! /bin/bash
#
# LICENSE：GPL v2
# Author: Y.H. Liu
# Last Modified： 2011-4-26
# Version: 0.2.1
# 本程式不保證任何運作結果之正確性！使用時，請自行負擔風險～
# 使用說明:
#   1. 若採用 IP 範圍進行流量管制；而 IP 範圍過大，FW 本機至少要雙核心以上才行。
#   2. 請先編輯本檔「參數設定區」各參數值。
#   3. 限用於 NAT 或 Bridge Mode 防火牆（網路咽喉點）上，要填寫正確的 FWTYPE 才行
#   4. 務必要填管制類型：IP範圍、MAC鎖定
#   5. 修改完畢，在終端機底下以 root 身份執行。
#      fwtc start 啟動
#      fwtc stop  中止
#      fwtc restart 重新啟動（適用於參數修改後）
#      fwtc show 目前流量規則顯示



LANG="zh_TW.UTF-8"
PATH="/sbin:/usr/sbin:/bin:/usr/bin"

#----------------------- 共用參數設定區------------------------------------
#上傳限制網卡；公用 IP 或 Bridge 對外（連接路由端）
DEV_UP="eth0"

#下載限制網卡；私有 IP 或 Bridge Mode 的內網（連集線器端至全部內網）
DEV_DW="eth1"

#防火牆種類，限填："nat" 或 "bridge"； 註：bridge 指的是透通式防火牆，IN/OUT 皆實體 IP
FWTYPE="nat"

#管制類型：限填："ipr", "mac"，分別指的是「IP範圍」或「網卡MAC位址」
TCTYPE="ipr"

#對外上傳實際最大頻寬，單位為 mbit 或 kbit
UPMAX="100mbit"

#對外下載實際最大頻寬，單位為 mbit 或 kbit
DWMAX="100mbit"

#每台 Client 流量限制，注意此處的計量單位是 kbytes/秒
##上傳保證頻寬（不可以太大），最好直接由「最大頻寬 / Client數」
UpRate="100kbps"
##上傳最大頻寬
UpCeil="400kbps"
##下載保證頻寬（不可以太大），最好直接由「最大頻寬 / Client數」
DwRate="200kbps"
##下載最大頻寬
DwCeil="800kbps"
#-----------------------------------------------------------------------


#------------------------- 選用 IP 範圍（ipr）設定區-----------------------------
#控制網段，請填 IPv4 網段前三碼再加「.」，例 "192.168.1."
NETC="192.168.110."

#起始 IP
IPS="2"

#結束 IP
IPE="254"
#-----------------------------------------------------------------------

# 在 BridgeMode FW 使用 nmap -sP 163.26.182.0/24  查出的 mac address------------

#------------------------ 選用 mac 管控（mac）設定區-----------------------------
#每個 mac address: (1).獨立一列，(2).大寫；下列內容為書寫範例
MACL="
00:50:7F:AB:XX:XX
D0:27:88:23:XX:XX
"
#-----------------------------------------------------------------------

function chkipv4()
{
   if [[ $1<1 || $1>254 ]]; then
      echo "F"
   else
      echo "T"
   fi
}


function chkmac()
{
   if [[ $1 =~ [A-F0-9][A-F0-9] ]]; then
      echo "T"
   else
      echo "F"
   fi
}


function tcstart()
{

   if [[ $TCTYPE == "ipr" ]]; then
      for ((i=$IPS; i<=$IPE; i++))
      do
         if [[ $FWTYPE == "bridge" ]]; then
            #上傳
            iptables -t mangle -A FORWARD -d ${NETC}${i} -m physdev --physdev-in $DEV_DW --physdev-out $DEV_UP -j MARK --set-mark ${i}0
            #下載
            iptables -t mangle -A FORWARD -s ${NETC}${i} -m physdev --physdev-in $DEV_UP --physdev-out $DEV_DW -j MARK --set-mark ${i}5

         elif [[ $FWTYPE == "nat" ]]; then
            #上傳 set mark
            iptables -t mangle -A PREROUTING -s ${NETC}${i} -j MARK --set-mark ${i}0
            #下載 set mark
            iptables -t mangle -A FORWARD -d ${NETC}${i} -j MARK --set-mark ${i}5
         fi
      done
   elif [[ $TCTYPE == "mac" ]]; then
      i=1
      for line in $MACL
      do
         if [[ $FWTYPE == "bridge" ]]; then
            #上傳
            iptables -t mangle -A FORWARD -m mac --mac-source $line -m physdev --physdev-in $DEV_DW --physdev-out $DEV_UP -j MARK --set-mark ${i}0
            #下載
            iptables -t mangle -A FORWARD -m mac --mac-source $line -m physdev --physdev-in $DEV_UP --physdev-out $DEV_DW -j MARK --set-mark ${i}5
         elif [[ $FWTYPE == "nat" ]]; then
            #上傳 set mark
            iptables -t mangle -A PREROUTING -m mac --mac-source $line -j MARK --set-mark ${i}0
            #下載 set mark
            iptables -t mangle -A FORWARD -m mac --mac-source $line -j MARK --set-mark ${i}5
         fi
         ((i++))
      done
   fi

   # 上傳--總體設定----------------------------------------------------------
   # 清除 $DEV_UP 所有佇列規則
   tc qdisc del dev $DEV_UP root 2>/dev/null
   # 定義最頂層(根)佇列規則，並指定 default 類別編號
   tc qdisc add dev $DEV_UP root handle 10: htb default ${i}0
   # 定義第一層的 10:1 類別 (總頻寬)
   tc class add dev $DEV_UP parent 10:  classid 10:1 htb rate $UPMAX ceil $DWMAX
   
   # 下載--總體設定----------------------------------------------------------
   # 清除 DEV_DW 所有佇列規則
   tc qdisc del dev $DEV_DW root 2>/dev/null
   # 定義最頂層(根)佇列規則，並指定 default 類別編號
   tc qdisc add dev $DEV_DW root handle 10: htb default ${i}5
   # 定義第一層的 10:1 類別 (總頻寬)
   tc class add dev $DEV_DW parent 10:  classid 10:1 htb rate $UPMAX ceil $DWMAX


   if [[ $TCTYPE == "ipr" ]]; then
      for ((i=$IPS; i<=$IPE; i++))
      do
         mHandle=$((i+100))
         # 上傳之 rate 保證頻寬，ceil 最大頻寬，prio 優先權
         tc class add dev $DEV_UP parent 10:1 classid 10:${i}0 htb rate $UpRate ceil $UpCeil prio 3
         # 定義各葉類別的佇列規則
         # parent 類別編號，handle 葉類別佇列規則編號, 由於採用 fw 過濾器，所以此處使用 pfifo 的佇列規則即可
         tc qdisc add dev $DEV_UP parent 10:${i}0 handle $mHandle: pfifo
         # 設定過濾器: 指定貼有 10 標籤 (handle) 的封包，歸類到 10:10 類別，以此類推
         tc filter add dev $DEV_UP parent 10: protocol ip prio 10 handle ${i}0 fw classid 10:${i}0

         # 下載之 rate 保證頻寬，ceil 最大頻寬，prio 優先權
         tc class add dev $DEV_DW parent 10:1 classid 10:${i}0 htb rate $DwRate ceil $DwCeil prio 2
         # 定義各葉類別的佇列規則
         # parent 類別編號，handle 葉類別佇列規則編號, 由於採用 fw 過濾器，所以此處使用 pfifo 的佇列規則即可
         tc qdisc add dev $DEV_DW parent 10:${i}0 handle $mHandle: pfifo
         # 設定過濾器: 指定貼有 10 標籤 (handle) 的封包，歸類到 10:10 類別，以此類推
         tc filter add dev $DEV_DW parent 10: protocol ip prio 10 handle ${i}5 fw classid 10:${i}0
      done
   elif [[ $TCTYPE == "mac" ]]; then
      i=1
      for line in $MACL
      do
         mHandle=$((i+100))
         # 上傳之 rate 保證頻寬，ceil 最大頻寬，prio 優先權
         tc class add dev $DEV_UP parent 10:1 classid 10:${i}0 htb rate $UpRate ceil $UpCeil prio 3
         # 定義各葉類別的佇列規則
         # parent 類別編號，handle 葉類別佇列規則編號, 由於採用 fw 過濾器，所以此處使用 pfifo 的佇列規則即可
         tc qdisc add dev $DEV_UP parent 10:${i}0 handle $mHandle: pfifo
         # 設定過濾器: 指定貼有 10 標籤 (handle) 的封包，歸類到 10:10 類別，以此類推
         tc filter add dev $DEV_UP parent 10: protocol ip prio 10 handle ${i}0 fw classid 10:${i}0

         # 下載之 rate 保證頻寬，ceil 最大頻寬，prio 優先權
         tc class add dev $DEV_DW parent 10:1 classid 10:${i}0 htb rate $DwRate ceil $DwCeil prio 2
         # 定義各葉類別的佇列規則
         # parent 類別編號，handle 葉類別佇列規則編號, 由於採用 fw 過濾器，所以此處使用 pfifo 的佇列規則即可
         tc qdisc add dev $DEV_DW parent 10:${i}0 handle $mHandle: pfifo
         # 設定過濾器: 指定貼有 10 標籤 (handle) 的封包，歸類到 10:10 類別，以此類推
         tc filter add dev $DEV_DW parent 10: protocol ip prio 10 handle ${i}5 fw classid 10:${i}0

         ((i++))
      done
   fi
}



function tcstop()
{
   # Flush mangle, 注意: 若其他 shell 存在 mangle 規則列，下列兩行要註解
   iptables -F -t mangle
   iptables -t mangle -X
   # flush tc qdisc 清空 tc 規則佇列，註： 2>/dev/null,send stderr to /dev/null
   tc qdisc del dev $DEV_UP root 2>/dev/null
   tc qdisc del dev $DEV_DW root 2>/dev/null
}


case "$1" in
   start)
         isDataOK="T"
         echo "檢查參數之設定是否正確中..."
         if [[ $TCTYPE == "ipr" ]];then
            if [[ $NETC == *[.]  ]]; then
               isDataOK="T"
            else
               echo "網段前三碼最後要加「.」，請修改後再啟動"
               isDataOK="F"
            fi
            #檢查 IPv4 數字是否介於 1-254 之間
            IFS="."
            for k in $NETC
            do
               if [[ $(chkipv4 $k) == "F" ]]; then
                  echo "網段前三碼之 IPv4 位址不合理，請修改後再啟動"
                  isDataOK="F"
               fi
            done
            if [[ $(chkipv4 $IPS) == "F" ]]; then
               echo "起始 IPS 值設定有誤"
               isDataOK="F"
            fi
            if [[ $(chkipv4 $IPE) == "F" ]]; then
               echo "結束 IPE 值設定有誤"
               isDataOK="F"
            fi
            unset IFS
         elif [[ $TCTYPE == "mac" ]]; then
            nk=1
            for line in $MACL
            do
               IFS=":"
               for k in $line
               do
                     if [[ $(chkmac $k) == "F" ]]; then
                        echo "  第${nk}筆 MAC 位址 ${k} 寫法不合理，請檢查!"
                        isDataOK="F"
                     fi
                  
               done
               ((nk++))
               unset IFS
            done
         fi

         if [[ $isDataOK == "T" ]];then
            tcstart
            echo "成功啟動流量管理措施..."
         else
            echo "啟動失敗"
         fi
   ;;
   stop)
         echo "中止流量管制措施..."
         tcstop
   ;;
   restart)
         echo "停止流量管制措施..."
         tcstop
         echo "啟動流量管到措施..."
         tcstart
   ;;
   show)
         echo "目前流量管制措施規則如下："
         tc qdisc show
   ;;
   *)
         echo "Usage: fwtc {start|stop|restart|show}"
         exit 1
   ;;
esac

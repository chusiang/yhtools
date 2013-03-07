#!/bin/bash
#
# 版權宣告：GPL 2.0
# 最後修訂： 2011-3-11
# Version: 0.2
# 本程式不保證任何運作結果之正確性！使用時，請自行負擔風險～

LANG=zh_TW.UTF-8
PATH=/usr/local/bin:/usr/bin:/bin
action="$1"
pubfolder="$2"

cd /home
if [ ! -d ftp ]; then
   mkdir ftp
fi
fnames=$(ls /home)
for i in $fnames
do
   if [ -d $i ]; then
      cd $i
      if [ "$action" == "-m" ]; then
         if [ ! -d $pubfolder ]; then
            mkdir $pubfolder
            chmod 1777 $pubfolder
         fi
         ismount=$(mount |awk '{print $3}' |grep /home/$i/$pubfolder)
         if [[ "$ismount" != "/home/$i/$pubfolder" &&  "$i" != "ftp" ]]; then
            mount --bind /home/ftp/$pubfolder ./$pubfolder
         fi
      elif [ "$action" == "-u" ]; then
         ismount=$(mount |awk '{print $3}' |grep /home/$i/$pubfolder)
         if [[ "$ismount"=="/home/$i/$pubfolder" ]]; then
            umount /home/$i/$pubfolder
         fi
      else
         export err="yes"
      fi
      cd ..
   fi
done
if [ "$err" == "yes" ]; then
   echo "usage: /path/to/pubfolder.sh -m|-u 資料夾名稱( -m 掛載；-u 移除 )"
fi

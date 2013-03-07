#!/bin/bash

# 版權：GPL 2.0
# 最後修訂： 2011-05-05
# Version: 0.2.1
# 本人不保證任何程式碼之正確性！使用時，請自行負擔風險～
#
# 請先執行 dos2unix passwd.txt 轉換成 unix 看得懂的純文字模式
#
# 
export LANG=zh_TW.UTF-8
export PATH=/sbin:/usr/sbin:/bin:/usr/bin
accountfile=""
if [ -f "$2" ]; then
   accountfile="$2"
else
   echo "找不到帳號密碼檔, 請先閱讀 readme.txt, 再使用本功能!"
   exit 1
fi


case "$1" in
   add)
      # 開始建立帳號與密碼！
      while read user pass
      do

	 if [ -n "$user" ]; then 
		 echo "account--> $user creating..."
		 useradd -m -s /bin/bash $user
		 echo "change $user password with password--> $pass"
		 echo "$user:$pass" | chpasswd
		 /bin/mkdir /home/$user/public_html
		 echo "<br><h2 align='center'>這是  $user 的個人首頁</h2>" > /home/$user/public_html/index.html
		 /bin/chown -R $user.$user /home/$user/public_html
	 fi

	 if [ "$3" == "smbsync" ]; then
		 tmpfile=$(mktemp)
		 echo $pass > $tmpfile
		 echo $pass >> $tmpfile
		 pdbedit -au "$user" -t < $tmpfile
		 [ -f $tmpfile ] && rm -f $tmpfile
	 fi

      # 請參考 "行程管理" 的 "行程替換" 
      done < <(awk -F: '{print $1, $2}' < $accountfile)

    ;;
   mysql)
      # 開始建立資料庫及MySQL使用者帳號與密碼！
      read -p "請輸入資料庫 root 密碼：" mysqlpass
      passok=$(/usr/bin/mysqladmin -uroot -p$mysqlpass status | cut -d ':' -f 1)
      if [ "$passok" == "Uptime" ]; then
          while read user pass
          do

	     if [ -n "$user" ]; then 
		    /usr/bin/mysql -u root -p$mysqlpass --execute="CREATE DATABASE $user;
		    GRANT ALL PRIVILEGES ON $user.* TO '$user'@'localhost' IDENTIFIED BY '$pass';"
	     fi

	     if [ "$3" == "smbsync" ]; then
		    tmpfile=$(mktemp)
		    echo $pass > $tmpfile
		    echo $pass >> $tmpfile
		    pdbedit -au "$user" -t < $tmpfile
		    [ -f $tmpfile ] && rm -f $tmpfile
	     fi

          # 請參考 "行程管理" 的 "行程替換" 
          done < <(awk -F: '{print $1, $2}' < $accountfile)
      else
          echo "資料庫 root 密碼有誤，無法執行"
      fi
    ;;
   del)
      usernames=$(cat "$accountfile" | cut -d ':' -f 1)
      for username in $usernames
      do
	 echo "userdel -r $username"
	 if [ "$3" == "smbsync" ]; then
	 	pdbedit -xu $username
	 fi
		userdel -r $username
      done
    ;;
   *)
     echo "Usage: maccount.sh {add|mysql|del} 帳號密碼檔.txt smbsync"
     exit 1
esac

#!/bin/bash
#
# 版權宣告：GPL 2.0
# 最後修訂： 2011-05-10
# Version: 0.1
# 本程式不保證任何運作結果之正確性！使用時，請自行負擔風險～
# 功能：有時會遇到某個資料夾權限為 700 ，但想把其修改成 755 或 777
#      全部的人可讀寫(777)時，資料夾會設為 777 檔案 666
#      別人只可讀時(755) ，資料夾會設為 755 檔案 644 
# 注意：若有執行權需求，勿用

LANG=zh_TW.UTF-8
PATH=/usr/local/bin:/usr/bin:/bin

# 有使用遞迴
do_chmod() {
	local mydtype
	local mydname
	local allname1
	mydtype="$1"
    mydname="$2"
    # echo "dtype:"$mydtype"  dname:"$mydname
    cd $mydname
    allname=$(ls)
    for i in $allname
    do
        if [ -d $i ]; then
            if [ "$mydtype" == "777" ]; then
                chmod 777 $i
            elif [ "$mydtype" == "755" ]; then
                chmod 755 $i
            fi
            do_chmod "$mydtype" "$i"
        else
            if [ "$mydtype" == "777" ]; then
                chmod 666 $i
            elif [ "$mydtype" == "755" ]; then
                chmod 644 $i
            fi
        fi
    done
    cd ../
}

argok="T"

if [ "$1" == "" ] || [ "$2" == "" ]; then
    argok="F"
else
    dtype="$1"
    dname="$2"
fi

if [ $argok == "T" ]; then
    ypath=$(pwd)

    if ([ "$dtype" == "777" ] || [ "$dtype" == "755" ]) && [ -d $dname ]; then
        read -p "目前所處的資料夾位置: "$ypath"；要對資料夾："$dname" 更改權限為 $dtype(y/n):" ifproc
        if [ "$ifproc" == "Y" ] || [ "$ifproc" == "y" ]; then
            if [ "$dtype" == "777" ]; then
                chmod 777 $dname
            elif [ "$dtype" == "755" ]; then
                chmod 755 $dname
            fi
            do_chmod "$dtype" "$dname"
        fi
    else
        echo "參數錯誤，使用方法： ./chmodadv.sh 777|755 資料夾名稱"
    fi
else
     echo "參數錯誤，使用方法： ./chmodadv.sh 777|755 資料夾名稱"
fi

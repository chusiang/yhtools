#! /bin/bash
LANG=zh_TW.UTF-8
PATH=/usr/local/bin:/usr/bin:/bin

oripath=$(pwd)
cd /home
fnames=$(ls)
for i in $fnames
do
    if [ -d $i ]; then
       chown -R $i.$i $i
    fi
done
cd $oripath

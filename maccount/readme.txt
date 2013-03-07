程式名稱: maccount.sh
用途：大量建帳號, 並可與 samba 密碼同步
語系：中文 utf-8
適用OS： ubuntu 10.10 以上/debian squeeze /ob2d sqz
其他系統未經測試, 不知是否會有問題

使用方法：
1. 先建立一個帳號密碼的純文字檔, 格式如下
   username_a:password_1
   username_b:password_2

   (1).假設檔名為 passwd.txt
   (2).大量建帳號前，先使用「dos2unix passwd.txt」指
       令把 passwd.txt 內的斷行符號確定轉成 unix 格式
       以利 BASH 可以正確處理文字。

2. 以 root 身份執行 maccount.sh, 後面必須接三個參數
   (1). add|del 建立或刪除
   (2). 檔名(ex. passwd.txt)
   (3). smbsync 是否與 SAMBA 同步

3. 舉例如下：
   (1). 僅大量建帳號, 不同步至 SAMBA
        ./maccount.sh add passwd.txt
   (2). 大量建帳號, 並同步至 SAMBA
        ./maccount.sh add passwd.txt smbsync
   (3). 大量刪除帳號(沒有 SAMBA 同步問題)
        ./maccount.sh del passwd.txt
   (4). 大量刪除帳號, 並結束與 SAMBA 同步
        ./maccount.sh del passwd.txt smbsync
   (5). 同步建立 mysql db 及 user 帳號
        ./maccount.sh mysql passwd.txt

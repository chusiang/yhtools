#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# License: GPL v2
# Language: zh_TW.utf8
# Version: 0.1.3
# Last modified: 2011-04-22
# Author: Y.H.Liu
import subprocess, os
from tkinter import *
from tkinter.messagebox import *

class MainWindow(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.if_out_Var = StringVar()
		self.if_in_Var = StringVar()
		self.fmod_Var = StringVar()
		self.ip4addr_Var = StringVar()
		self.ip4mask_Var = StringVar()
		self.ip4gate_Var = StringVar()
		self.ip4broad_Var = StringVar()
		self.ip4net_Var = StringVar()
		self.serv022_Var = StringVar()
		self.serv023_Var = StringVar()
		self.serv873_Var = StringVar()
		self.serv993_Var = StringVar()
		self.serv995_Var = StringVar()
		# 5900-5905
		self.serv5900_Var = StringVar()
		# 8080-8081
		self.serv8080_Var = StringVar()
		self.LooseRules = '''
# 預設政策，全開
$IPTABLES -P INPUT ACCEPT
$IPTABLES -P OUTPUT ACCEPT
$IPTABLES -P FORWARD ACCEPT

###--------------------------------------------------------------###
# 鎖 mac address 使防火牆內部的電腦無法上網
# 註：一定要把鎖 MAC 的規則列寫在目前範例所示的位置, 否則會失效
###--------------------------------------------------------------###
# $IPTABLES -A FORWARD -o $FW_IFACE -p tcp -m mac --mac-source xx:xx:xx:xx:xx:xx -j DROP

###---------------------------------------------------------------###
# 以下是針對外面要存取 fw 本機的連線限制示例
###---------------------------------------------------------------###
# 只有本主機所屬網段才能連到這台主機的 ssh port 22
$IPTABLES -A INPUT -p tcp -s {ip4net} --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp --dport 22 -j DROP

		'''
		
		self.StrictRules = '''
# 預設政策，中止封包轉送，只開放必要的
$IPTABLES -P INPUT ACCEPT
$IPTABLES -P OUTPUT ACCEPT
$IPTABLES -P FORWARD DROP

###--------------------------------------------------------------###
# 鎖 mac address 使防火牆內部的電腦無法上網
# 註：一定要寫在最開頭的位置, 否則會失效
###--------------------------------------------------------------###
# $IPTABLES -A FORWARD -o $FW_IFACE -p tcp -m mac --mac-source xx:xx:xx:xx:xx:xx -j DROP

###-----------------------------------------------------###
# open 對內部機器可以取得外面 DHCP 功能
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p udp --sport 68 --dport 67 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p udp --sport 67 --dport 68 -j ACCEPT

###-----------------------------------------------------###
# open DNS port 53
###-----------------------------------------------------###
# 第一次會用 udp 封包來查詢
$IPTABLES -A FORWARD -o $FW_IFACE -p udp --sport 1024:65535 --dport 53 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p udp --sport 53 --dport 1024:65535 -j ACCEPT

# 若有錯誤，會改用 tcp 封包來查詢
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 53 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 53 --dport 1024:65535 -j ACCEPT

# 開放這台主機上的 DNS 和外部的 DNS 主機互動查詢：使用 udp
$IPTABLES -A FORWARD -p udp -s $FW_IP --sport 53 -d any/0 --dport 53 -j ACCEPT
$IPTABLES -A FORWARD -p udp -s any/0 --sport 53 -d $FW_IP --dport 53 -j ACCEPT
# 開放這台主機上的 DNS 和外部的 DNS 主機互動查詢：使用 tcp
$IPTABLES -A FORWARD -p tcp -s $FW_IP --sport 53 -d any/0 --dport 53 -j ACCEPT
$IPTABLES -A FORWARD -p tcp ! --syn -s any/0 --sport 53 -d $FW_IP --dport 53 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機 ftp port 21
###-----------------------------------------------------###
# 以下是打開命令 channel 21
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 21 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 21 --dport 1024:65535 -j ACCEPT

# 以下是打開資料 channel 20
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp --sport 20 --dport 1024:65535 -j ACCEPT
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp ! --syn --sport 1024:65535 --dport 20 -j ACCEPT

# 以下是打開 passive mode FTP 資料通道
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 1024:65535 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 1024:65535 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的 SMTP port 25
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 25 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 25 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的 HTTP port 80
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 80 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 80 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的 HTTPs port 443
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 443 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 443 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的 POP3 port 110
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 110 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 110 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的 IMAP port 143
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 143 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 143 --dport 1024:65535 -j ACCEPT

###-----------------------------------------------------###
# open 對外部主機的網路校時 ntpdate port 123
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport 123 -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport 123 --dport 1024:65535 -j ACCEPT'''
		
		self.StrictRules2 = '''

###---------------------------------------------------------------###
# 以下是針對外面要存取 fw 本機的連線限制示例
###---------------------------------------------------------------###
# 只有本主機所屬網段才能連到這台主機的 ssh port 22
$IPTABLES -A INPUT -p tcp -s {ip4net} --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp --dport 22 -j DROP'''

		
		self.RcLocal = '''#! /bin/bash
#
# 本 Script 參考自 OLS3 (ols3@lxer.idv.tw)
# 本 Script 受 /etc/init.d/rc.local 控管，切勿刪除最後一行「exit 0」
# Ubuntu 10.x 及 Debian lenny 之後版本，直接以本檔覆蓋 /etc/rc.local 
# 執行 service rc.local start 套用新規列
#

IPTABLES="/sbin/iptables"
IP6TABLES="/sbin/ip6tables"

BRCTL="/usr/sbin/brctl"
IFCONFIG="/sbin/ifconfig"
ROUTE="/sbin/route"

BRIP="{ip4addr}"
FW_IP="{ip4addr}"
BRMASK="{ip4mask}"
GATEWAY="{ip4gate}"
BRBROADCAST="{ip4broad}"

FW_IFACE="br0"


# 先關閉這三組網路介面
{if_in}exist=$(/sbin/ifconfig |grep "{if_in}")
if [ "${if_in}exist" != "" ]; then
    $IFCONFIG {if_in} down
fi

{if_out}exist=$(/sbin/ifconfig |grep "{if_out}")
if [ "${if_out}exist" != "" ]; then
    $IFCONFIG {if_out} down
fi

br0exist=$(/sbin/ifconfig |grep "br0")
if [ "$br0exist" != "" ]; then
    $IFCONFIG br0 down
    # 再關閉 birdge 的 binding
    $BRCTL delif br0 {if_in}
    $BRCTL delif br0 {if_out}
    $BRCTL delbr br0
fi


# 設定 {if_out} 及 {if_in} 網卡介面
$IFCONFIG {if_out} 0.0.0.0
$IFCONFIG {if_in} 0.0.0.0

#啟動 bridge 與 網卡的 Binding
$BRCTL addbr br0
$BRCTL addif br0 {if_out}
$BRCTL addif br0 {if_in}

# 設定 br0 介面
$IFCONFIG br0 $BRIP netmask $BRMASK broadcast $BRBROADCAST


# 設定 gateway 值，使 fw 本身可以上網　
$ROUTE add default gw $GATEWAY

# 啟動封包轉送
echo "1" > /proc/sys/net/ipv4/ip_forward


###-----------------------------------------------------###
# 清除先前的設定
###-----------------------------------------------------###
echo "Flush fiter table ......"
echo

# Flush filter
$IPTABLES -F
$IPTABLES -X
$IP6TABLES -F

echo "Flush mangle table ......"
echo
# Flush mangle
$IPTABLES -F -t mangle
$IPTABLES -t mangle -X


echo "Flush nat table ......"
echo
# Flush nat
$IPTABLES -F -t nat
$IPTABLES -t nat -X

		'''
		
		fmod_Label = Label(self, text="預設政策：",font=( None, 12), width=12)
		fmod1_RB = Radiobutton(self, text="全部放行", variable=self.fmod_Var, value="loose", font=( None, 12),width=16)
		fmod2_RB = Radiobutton(self, text="嚴格鎖埠", variable=self.fmod_Var, value="strict", font=( None, 12))
		self.fmod_Var.set("loose")
		blank1_Label = Label(self, text=" ", width=2)
		blank2_Label = Label(self, text=" ", width=2)
		blank3_Label = Label(self, text=" ", width=2)
		DocLabel_1 = Label(self, text="基本設定", bg='blue', fg='white', font=( None, 12), width=54)
		if_out_Label = Label(self, text="對外網卡(eth0):", width=12, anchor=E)
		if_out_Entry = Entry(self, textvariable=self.if_out_Var, width=16)
		if_out_Entry.focus_set()
		self.if_out_Var.set("eth0")
		if_in_Label = Label(self, text="對內網卡(eth1):", width=12, anchor=E)
		if_in_Entry = Entry(self, textvariable=self.if_in_Var, width=16)
		self.if_in_Var.set("eth1")
		ip4mask_Label = Label(self, text="遮罩:", width=12, anchor=E)
		ip4mask_Entry = Entry(self, textvariable=self.ip4mask_Var, width=16)
		ip4maskdoc_Label = Label(self, text="(例:255.255.255.0)" )
		self.ip4mask_Var.set("255.255.255.")
		ip4broad_Label = Label(self, text="廣播:", width=12, anchor=E)
		ip4broad_Entry = Entry(self, textvariable=self.ip4broad_Var, width=16 )
		ip4broaddoc_Label = Label(self, text="(例:163.26.182.255)" )
		ip4net_Label = Label(self, text="網段:", width=12, anchor=E)
		ip4net_Entry = Entry(self, textvariable=self.ip4net_Var, width=16)
		ip4netdoc_Label = Label(self, text="(例:163.26.182.0/24)" )
		ip4addr_Label = Label(self, text="IPv4位址:", anchor=E)
		ip4addr_Entry = Entry(self, textvariable=self.ip4addr_Var, width=15)
		ip4gate_Label = Label(self, text="GateWay:", anchor=E)
		ip4gate_Entry = Entry(self, textvariable=self.ip4gate_Var, width=15)
		DocLabel_2 = Label(self, text="（阻擋外部網路連線至本機 port 22 之阻擋規則為預設值）")
		DocLabel_3 = Label(self, text="   ")
		DocLabel_4 = Label(self, text="選「鎖埠政策」請繼續勾選要放行的服務", bg='blue', fg='white', font=( None, 12), width=54)
		serv022_CB = Checkbutton(self, text="SSH_22   ", variable=self.serv022_Var, onvalue="T", offvalue="F", width=12, anchor=W)
		serv023_CB = Checkbutton(self, text="telnet_23", variable=self.serv023_Var, onvalue="T", offvalue="F", width=16, anchor=W)
		serv993_CB = Checkbutton(self, text="POP3s_993", variable=self.serv993_Var, onvalue="T", offvalue="F", anchor=W)
		serv995_CB = Checkbutton(self, text="IMAPs_995", variable=self.serv995_Var, onvalue="T", offvalue="F", anchor=W)
		serv873_CB = Checkbutton(self, text="rSync_873", variable=self.serv873_Var, onvalue="T", offvalue="F", anchor=W, width=12)
		serv5900_CB = Checkbutton(self, text="5900-5905", variable=self.serv5900_Var, onvalue="T", offvalue="F", width=16, anchor=W)
		serv8080_CB = Checkbutton(self, text="8080-8081", variable=self.serv8080_Var, onvalue="T", offvalue="F", anchor=W)
		DocLabel_5 = Label(self, text="（預設放行埠：DHCP, DNS, http, https, FTP, SMTP, POP3, IMAP, NTP）")
		
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_6 = Label(self, text="（按 Escape 鍵離開）")
		
		fmod_Label.grid(row=0, column=0, sticky=E, pady=3, padx=3, ipady=3, ipadx=3)
		fmod1_RB.grid(row=0, column=1, sticky=E, pady=3, padx=3, ipady=3, ipadx=3)
		fmod2_RB.grid(row=0, column=2, columnspan=3, sticky=W, pady=3, padx=3, ipady=3, ipadx=3)
		DocLabel_1.grid(row=1, column=0, columnspan=5, pady=3, padx=3, ipady=3, ipadx=3 )
		if_out_Label.grid(row=2, column=0, sticky=E, pady=3, padx=3)
		if_out_Entry.grid(row=2, column=1, sticky=W, pady=3, padx=3)
		ip4addr_Label.grid(row=2, column=2, sticky=E, pady=3, padx=3)
		ip4addr_Entry.grid(row=2, column=3, sticky=EW, pady=3, padx=3)
		blank1_Label.grid(row=2, column=4, pady=3,padx=3)
		if_in_Label.grid(row=3, column=0, sticky=E, pady=3, padx=3)
		if_in_Entry.grid(row=3, column=1, sticky=W, pady=3, padx=3)
		ip4gate_Label.grid(row=3, column=2, sticky=E, pady=3, padx=3)
		ip4gate_Entry.grid(row=3, column=3, sticky=EW, pady=3, padx=3)
		blank2_Label.grid(row=2, column=4, pady=3,padx=3)
		ip4mask_Label.grid(row=4, column=0, sticky=E, pady=3, padx=3)
		ip4mask_Entry.grid(row=4, column=1, sticky=W, pady=3, padx=3)
		ip4maskdoc_Label.grid(row=4, column=2, columnspan=3, sticky=W, pady=3, padx=3)
		ip4broad_Label.grid(row=5, column=0, sticky=E, pady=3, padx=3)
		ip4broad_Entry.grid(row=5, column=1, sticky=W, pady=3, padx=3)
		ip4broaddoc_Label.grid(row=5, column=2, columnspan=3, sticky=W, pady=3, padx=3)
		ip4net_Label.grid(row=6, column=0, sticky=E, pady=3, padx=3)
		ip4net_Entry.grid(row=6, column=1, sticky=W, pady=3, padx=3)
		ip4netdoc_Label.grid(row=6, column=2, columnspan=3, sticky=W, pady=3, padx=3)
		DocLabel_2.grid(row=7, column=0, columnspan=5, pady=3, padx=3)
		DocLabel_3.grid(row=8, column=0, columnspan=5, pady=3, padx=3)
		DocLabel_4.grid(row=9, column=0, columnspan=5, pady=3, padx=3, ipady=3, ipadx=3)
		serv022_CB.grid(row=10, column=0, sticky=W, pady=3, padx=12)
		serv023_CB.grid(row=10, column=1, sticky=W, pady=3, padx=12)
		serv993_CB.grid(row=10, column=2, sticky=W, pady=3, padx=12)
		serv995_CB.grid(row=10, column=3, sticky=W, pady=3, padx=12)
		blank3_Label.grid(row=10, column=4, pady=3,padx=3)
		serv873_CB.grid(row=11, column=0, sticky=W, pady=3, padx=12)
		serv5900_CB.grid(row=11, column=1, sticky=W, pady=3, padx=12)
		serv8080_CB.grid(row=11, column=2, columnspan=3, sticky=W, pady=3, padx=12)
		
		okButton.grid(row=12, column=0, columnspan=5, pady=3, padx=3)
		DocLabel_5.grid(row=13, column=0, columnspan=5, pady=3, padx=3)
		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		self.grid(row=0, column=0, sticky=NSEW)
		self.columnconfigure(1, weight=1)
		
		self.master.bind("<Return>", self.ok)
		self.master.bind("<Escape>", self.close)
		
	
	def confw(self, fname, fcontent):
		fname = "./" + fname
		if os.path.isfile( fname ):
			subprocess.check_call(["/bin/rm", "-rf", fname])
		fh = None
		try:
			fh = open( fname , "w", encoding="utf8")
			fh.write( fcontent )
		except EnvironmentError as err:
			showerror(title="錯誤", message="無法寫入檔案")
		finally:
			if fh is not None:
				fh.close()
	
	def createRules(self, tcpport):
		Rules = '''

###-----------------------------------------------------###
# open 對外部主機的 port {tcpport}
###-----------------------------------------------------###
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --sport 1024:65535 --dport {tcpport} -j ACCEPT
$IPTABLES -A FORWARD -i $FW_IFACE -p tcp ! --syn --sport {tcpport} --dport 1024:65535 -j ACCEPT'''
		if tcpport == "5900":
			tcpport = "5900:5905"
		elif tcpport == "8080":
			tcpport = "8080:8081"
		Rules = Rules.format(**locals())
		self.StrictRules = self.StrictRules + Rules
	
	def chkipv4(self, ipvalue):
		strRes = "T"
		ip4list = ipvalue.split(".")
		if len(ip4list) != 4:
			strRes = "F"
		else:
			for i in range(4):
				if int(ip4list[i]) > 255:
					strRes = "F" 
		return strRes
	
	def ok(self, event=None):
		isdataok = "T"
		fmod = ""
		if_out = ""
		if_in = ""
		ip4addr = ""
		ip4mask = ""
		ip4gate = ""
		ip4net = ""
		ip4broad = ""
		serv022 = ""
		serv023 = ""
		serv993 = ""
		serv995 = ""
		serv873 = ""
		serv5900 = ""
		serv8080 = ""
		
		fmod = self.fmod_Var.get()
		if_out = self.if_out_Var.get()
		if_in = self.if_in_Var.get()
		ip4addr = self.ip4addr_Var.get()
		ip4mask = self.ip4mask_Var.get()
		ip4gate = self.ip4gate_Var.get()
		ip4net = self.ip4net_Var.get()
		ip4broad = self.ip4broad_Var.get()
		serv022 = self.serv022_Var.get()
		serv023 = self.serv023_Var.get()
		serv993 = self.serv993_Var.get()
		serv995 = self.serv995_Var.get()
		serv873 = self.serv873_Var.get()
		serv5900 = self.serv5900_Var.get()
		serv8080 = self.serv8080_Var.get()
		
		fmod = fmod.strip()
		if_out = if_out.strip()
		if_in = if_in.strip()
		ip4addr = ip4addr.strip()
		ip4mask = ip4mask.strip()
		ip4gate = ip4gate.strip()
		ip4net = ip4net.strip()
		ip4broad = ip4broad.strip()
		serv022 = serv022.strip()
		serv023 = serv023.strip()
		serv993 = serv993.strip()
		serv995 = serv995.strip()
		serv873 = serv873.strip()
		serv5900 = serv5900.strip()
		serv8080 = serv8080.strip()
		self.accpeted = True
		
		# data check 
		ip4net_a = ip4net.split("/")
		if fmod == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒指明要「全部放行」或「嚴格鎖埠」")
		elif if_out == "":
			isdataok = "F"
			showerror(title="資訊不足", message="對外網卡沒指定")
		elif if_in == "":
			isdataok = "F"
			showerror(title="資訊不足", message="對內網卡沒指定")
		elif ip4mask == "":
			isdataok = "F"
			showerror(title="資訊不足", message="遮罩沒填")
		elif self.chkipv4(ip4mask) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="遮罩格式不合理請檢查")
		elif ip4broad == "":
			isdataok = "F"
			showerror(title="資訊不足", message="廣播沒填")
		elif self.chkipv4(ip4broad) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="網路廣播格式不合理請檢查")
		elif ip4net == "":
			isdataok = "F"
			showerror(title="資訊不足", message="網段沒填")
		elif len(ip4net_a) != 2:
			isdataok = "F"
			showerror(title="錯誤", message="網段格式不合理請檢查")
		elif int(ip4net_a[1]) > 32:
			isdataok = "F"
			showerror(title="錯誤", message="網段格式不合理請檢查")
		elif self.chkipv4(ip4net_a[0]) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="網段格式不合理請檢查")
		elif ip4addr == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒填 IPv4 位址")
		elif self.chkipv4(ip4addr) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="IPv4 網址不合理請檢查")
		elif ip4gate == "":
			isdataok = "F"
			showerror(title="資訊不足", message="GateWay沒填")
		elif self.chkipv4(ip4gate) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="GateWay格式不合理請檢查")
		
		if isdataok == "T":
			if fmod == "strict":
				if serv022 == "T":
					self.createRules("22")
				if serv023 == "T":
					self.createRules("23")
				if serv993 == "T":
					self.createRules("993")
				if serv995 == "T":
					self.createRules("995")
				if serv873 == "T":
					self.createRules("873")
				if serv5900 == "T":
					self.createRules("5900")
				if serv8080 == "T":
					self.createRules("8080")
				self.RcLocal = self.RcLocal.format(**locals())
				self.StrictRules2 = self.StrictRules2.format(**locals())
				self.RcLocal = self.RcLocal + self.StrictRules + self.StrictRules2
			elif fmod == "loose":
				self.RcLocal = self.RcLocal.format(**locals())
				self.LooseRules = self.LooseRules.format(**locals())
				self.RcLocal = self.RcLocal + self.LooseRules
			self.RcLocal = self.RcLocal + "\n\n# 下面這一行切勿刪除\nexit 0"
			self.confw( "rc.local" , self.RcLocal )
			subprocess.check_call(["/bin/chmod", "+x", "rc.local"])
			showinfo( title="完工", message="防火牆設定檔已寫成 rc.local，請以 root 身份覆蓋 /etc/rc.local" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 280)
mY = int(scrY/2 - 205) - 60
strGeometry = "560x410+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("BridgeRoute 防火牆 rc.local 產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

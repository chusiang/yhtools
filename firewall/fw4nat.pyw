#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# License: GPL v2
# Language: zh_TW.utf8
# Version: 0.2.2
# Last modified: 2011-05-06
# Author: Y.H.Liu
import subprocess, os
from tkinter import *
from tkinter.messagebox import *

class MainWindow(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.fmod_Var = StringVar()
		self.out_if_Var = StringVar()
		self.out_ip4addr_Var = StringVar()
		self.out_ip4net_Var = StringVar()
		self.in_if_Var = StringVar()
		self.in_ip4addr_Var = StringVar()
		self.in_ip4net_Var = StringVar()
		self.serv022_Var = StringVar()
		self.serv023_Var = StringVar()
		self.serv873_Var = StringVar()
		self.serv993_Var = StringVar()
		self.serv995_Var = StringVar()
		# 5900-5905
		self.serv5900_Var = StringVar()
		# 8080-8081
		self.serv8080_Var = StringVar()
		self.CommonRules = '''#! /bin/bash
#
# iptables 範本
#
# 本 Script 參考自 OLS3 (ols3@lxer.idv.tw)
# 它由 /etc/init.d/rc.local 控管，切勿刪除最後一行「exit 0」
# Ubuntu 10.x 及 Debian lenny 之後版本，直接以本檔覆蓋 /etc/rc.local 
# 執行 service rc.local start 便可套用新規列
#
# 部分被註解的功能請自行參考修改，把註解拿掉即可啟用該項設定
#

###-----------------------------------------------------###
# 設定 iptables 的路徑
###-----------------------------------------------------###
echo
echo "Set path of iptables"
echo

IPTABLES="/sbin/iptables"

/sbin/modprobe ip_conntrack
/sbin/modprobe ip_conntrack_ftp
/sbin/modprobe iptable_nat
/sbin/modprobe ip_nat_ftp

###-----------------------------------------------------###
# 外部網段 IP 及介面
###-----------------------------------------------------###
echo "Set external ......"
echo

FW_IP="{out_ip4addr}"
FW_IP_RANGE="{out_ip4net}"
FW_IFACE="{out_if}"

###-----------------------------------------------------###
# 設定內部網段 IP 及介面
###-----------------------------------------------------###
echo "Set internal ......"
echo

LAN_IP="{in_ip4addr}"
LAN_IP_RANGE="{in_ip4net}"
LAN_IFACE="{in_if}"

# loopback interface
LO_IFACE="lo"
LO_IP="127.0.0.1"



###-----------------------------------------------------###
# 打開 forward
###-----------------------------------------------------###
#echo "Enable ip_forward ......"
#echo

echo "1" > /proc/sys/net/ipv4/ip_forward


###-----------------------------------------------------###
# 清除先前的設定
###-----------------------------------------------------###
echo "Flush fiter table ......"
echo

# Flush filter
$IPTABLES -F
$IPTABLES -X

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

###-----------------------------------------------------###
# 設定 filter table 的預設政策
###-----------------------------------------------------###
$IPTABLES -P INPUT ACCEPT
$IPTABLES -P OUTPUT ACCEPT
$IPTABLES -P FORWARD ACCEPT

###-----------------------------------------------------###
# 啟動內部對外轉址
###-----------------------------------------------------###

$IPTABLES -t nat -A POSTROUTING -o $FW_IFACE -j SNAT --to-source $FW_IP

###-----------------------------------------------------###
# 啟動外部對內部轉址
###-----------------------------------------------------###
# 凡對 $FW_IP:8080 連線者, 則轉址至 192.168.1.3:80
#$IPTABLES -t nat -A PREROUTING -p tcp -d $FW_IP --dport 8080  -j DNAT --to 192.168.1.3:80


###-----------------------------------------------------###
# 拒絕內部 IP 對外連線權力
###-----------------------------------------------------###

# 只允許某段 range ip 具上網權力，若採用嚴格鎖埠者，只要打開下面第一行即可
#$IPTABLES -A FORWARD -i $LAN_IFACE -p tcp -m iprange --src-range 192.168.110.128-192.168.110.150 -j ACCEPT
#$IPTABLES -A FORWARD -i $LAN_IFACE -p tcp -s 192.168.110.0/24 -j DROP


# 以下封掉內部主機連到外部主機的 port 6677, 請自行針對不同服務 port 號做修改
# 讓 192.168.1.6 通過
#$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s 192.168.110.6 --dport 6677 -j ACCEPT
# 其餘擋掉
#$IPTABLES -A FORWARD -o $FW_IFACE -p tcp --dport 6677 -j DROP


###-----------------------------------------------------###
# 以下封鎖外面的網站
###-----------------------------------------------------###
#$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -d 255.255.255.255 --dport 80 -j DROP


###-----------------------------------------------------###
# 封鎖內部某台 MAC 
###-----------------------------------------------------###
#$IPTABLES -A FORWARD -p tcp -m mac --mac-source xx:xx:xx:xx:xx:xx -j DROP


###-----------------------------------------------------###
# 控制某台電腦可用的每秒封包數（另一型式的流量管控）
###-----------------------------------------------------###
#$IPTABLES -A FORWARD -m mac --mac-source xx:xx:xx:xx:xx:xx -m limit --limit 60/s --limit-burst 65 -j ACCEPT
#$IPTABLES -A FORWARD -m mac --mac-source xx:xx:xx:xx:xx:xx -j DROP'''
		
		
		self.StrictRules = '''

#--------------------------------------------------------------------
# NAT對外連線鎖 TCP 埠，思考方向：不管進入封包，只管出去封包
# 被動式 ftp 在經過 port 21 協商後，開始傳資料時，會以本地端 1024:65535 對 ftp server:1024:65535溝通，只要限制
# 連線狀態為：「RELATED」及「ESTABLISHED」封包。即可避免 NAT 內電腦對外掃描，又可使用 FTP 服務
#--------------------------------------------------------------------
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 21 -j ACCEPT
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --sport 1024:65535 --dport 1024:65535 -m state --state RELATED,ESTABLISHED -j ACCEPT
# 對外 SMTP 寄信
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 25 -j ACCEPT
# 對外 DNS 查詢
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 53 -j ACCEPT
$IPTABLES -A FORWARD -o $FW_IFACE -p udp -s any/0 --dport 53 -j ACCEPT
# 對外瀏覽網頁
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 80 -j ACCEPT
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 443 -j ACCEPT
# POP3 收信
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 110 -j ACCEPT
# NTPDate 網路校時
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport 123 -j ACCEPT'''
		
		self.CommonRules2 = '''

###-----------------------------------------------------###
# 拒絕外部 IP 連至 fw 本機內部 port 號
###-----------------------------------------------------###

# 只有本主機所屬網段才能連到這台主機的 ssh port 22
$IPTABLES -A INPUT -p tcp -s {out_ip4net} --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp -s {in_ip4net} --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport 22 -j ACCEPT
$IPTABLES -A INPUT -p tcp --dport 22 -j DROP'''
		
		
		fmod_Label = Label(self, text="預設政策：",font=( None, 12), width=15)
		fmod1_RB = Radiobutton(self, text="全部放行", variable=self.fmod_Var, value="loose", font=( None, 12),width=16)
		fmod2_RB = Radiobutton(self, text="嚴格鎖埠", variable=self.fmod_Var, value="strict", font=( None, 12))
		self.fmod_Var.set("loose")
		blankL_Label = Label(self, text=" ", width=2)
		blank1_Label = Label(self, text=" ", width=2)
		blank2_Label = Label(self, text=" ", width=2)
		blank3_Label = Label(self, text=" ", width=2)
		blank4_Label = Label(self, text=" ", width=2)
		DocLabel_1 = Label(self, text="基本設定", bg='blue', fg='white', font=( None, 12), width=60)
		out_if_Label = Label(self, text="對外網卡(eth0):", width=15, anchor=E)
		out_if_Entry = Entry(self, textvariable=self.out_if_Var, width=16)
		out_if_Entry.focus_set()
		self.out_if_Var.set("eth0")
		out_ip4addr_Label = Label(self, text="公用IPv4位址:", width=15,anchor=E)
		out_ip4addr_Entry = Entry(self, textvariable=self.out_ip4addr_Var, width=16)
		out_ip4net_Label = Label(self, text="允許SSH之網址(段)一:", width=15,anchor=E)
		out_ip4net_Entry = Entry(self, textvariable=self.out_ip4net_Var, width=16)
		out_ip4netdoc_Label = Label(self, text="(例： 163.26.182.19 或 163.26.182.0/24)")
		in_if_Label = Label(self, text="對內網卡(eth1):", width=15, anchor=E)
		in_if_Entry = Entry(self, textvariable=self.in_if_Var, width=16)
		self.in_if_Var.set("eth1")
		in_ip4addr_Label = Label(self, text="私有IPv4位址:", width=15, anchor=E)
		in_ip4addr_Entry = Entry(self, textvariable=self.in_ip4addr_Var, width=16)
		in_ip4net_Label = Label(self, text="允許SSH之網址(段)二:", width=15,anchor=E)
		in_ip4net_Entry = Entry(self, textvariable=self.in_ip4net_Var, width=16)
		in_ip4netdoc_Label = Label(self, text="(例： 192.168.1.2 或 192.168.1.0/24)")
		DocLabel_2 = Label(self, text="（阻擋外部網路連線至本機 port 22 之阻擋規則為預設值）")
		DocLabel_3 = Label(self, text="   ")
		DocLabel_4 = Label(self, text="選「鎖埠政策」請繼續勾選要放行的服務", bg='blue', fg='white', font=( None, 12), width=60)
		serv022_CB = Checkbutton(self, text="SSH_22   ", variable=self.serv022_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv023_CB = Checkbutton(self, text="telnet_23", variable=self.serv023_Var, onvalue="T", offvalue="F", width=16, anchor=W)
		serv993_CB = Checkbutton(self, text="POP3s_993", variable=self.serv993_Var, onvalue="T", offvalue="F", anchor=W)
		serv995_CB = Checkbutton(self, text="IMAPs_995", variable=self.serv995_Var, onvalue="T", offvalue="F", anchor=W)
		serv873_CB = Checkbutton(self, text="rSync_873", variable=self.serv873_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv5900_CB = Checkbutton(self, text="5900-5905", variable=self.serv5900_Var, onvalue="T", offvalue="F", width=16, anchor=W)
		serv8080_CB = Checkbutton(self, text="8080-8081", variable=self.serv8080_Var, onvalue="T", offvalue="F", anchor=W)
		DocLabel_5 = Label(self, text="（預設放行埠：DNS, http, https, FTP, SMTP, POP3, IMAP, NTP）")
		
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_6 = Label(self, text="（按 Escape 鍵離開）")
		
		blankL_Label.grid(row=0, column=0, pady=3, padx=2)
		fmod_Label.grid(row=0, column=1, sticky=E, pady=3, padx=3, ipady=3, ipadx=3)
		fmod1_RB.grid(row=0, column=2, sticky=E, pady=3, padx=3, ipady=3, ipadx=3)
		fmod2_RB.grid(row=0, column=3, columnspan=3, sticky=W, pady=3, padx=3, ipady=3, ipadx=3)
		DocLabel_1.grid(row=1, column=0, columnspan=6, pady=3, padx=3, ipady=3, ipadx=3 )
		blankL_Label.grid(row=2, column=0, pady=3, padx=2)
		out_if_Label.grid(row=2, column=1, sticky=E, pady=3, padx=3)
		out_if_Entry.grid(row=2, column=2, sticky=W, pady=3, padx=3)
		in_if_Label.grid(row=2, column=3, sticky=E, pady=3, padx=3)
		in_if_Entry.grid(row=2, column=4, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=2, column=5, pady=3,padx=3)
		blankL_Label.grid(row=3, column=0, pady=3, padx=2)
		out_ip4addr_Label.grid(row=3, column=1, sticky=E, pady=3, padx=3)
		out_ip4addr_Entry.grid(row=3, column=2, sticky=W, pady=3, padx=3)
		in_ip4addr_Label.grid(row=3, column=3, sticky=E, pady=3, padx=3)
		in_ip4addr_Entry.grid(row=3, column=4, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=3, column=5, pady=3,padx=3)
		blankL_Label.grid(row=4, column=0, pady=3, padx=2)
		out_ip4net_Label.grid(row=4, column=1, sticky=E, pady=3, padx=3)
		out_ip4net_Entry.grid(row=4, column=2, sticky=W, pady=3, padx=3)
		in_ip4net_Label.grid(row=4, column=3, sticky=E, pady=3, padx=3)
		in_ip4net_Entry.grid(row=4, column=4, sticky=W, pady=3, padx=3)
		blank3_Label.grid(row=4, column=5, pady=3,padx=3)
		blankL_Label.grid(row=5, column=0, pady=3, padx=2)
		out_ip4netdoc_Label.grid(row=5, column=1, columnspan=2, sticky=EW, pady=3, padx=3)
		in_ip4netdoc_Label.grid(row=5, column=3, columnspan=2, sticky=EW, pady=3, padx=3)
		blank3_Label.grid(row=5, column=5, pady=3,padx=3)
		DocLabel_2.grid(row=6, column=0, columnspan=6, pady=3, padx=3)
		DocLabel_3.grid(row=7, column=0, columnspan=6, pady=3, padx=3)
		DocLabel_4.grid(row=8, column=0, columnspan=6, pady=3, padx=3, ipady=3, ipadx=3)
		blankL_Label.grid(row=9, column=0, pady=3, padx=2)
		serv022_CB.grid(row=9, column=1, sticky=W, pady=3, padx=3)
		serv023_CB.grid(row=9, column=2, sticky=W, pady=3, padx=3)
		serv993_CB.grid(row=9, column=3, sticky=W, pady=3, padx=3)
		serv995_CB.grid(row=9, column=4, sticky=W, pady=3, padx=3)
		blank4_Label.grid(row=9, column=5, pady=3,padx=3)
		blankL_Label.grid(row=10, column=0, pady=3, padx=2)
		serv873_CB.grid(row=10, column=1, sticky=W, pady=3, padx=3)
		serv5900_CB.grid(row=10, column=2, sticky=W, pady=3, padx=3)
		serv8080_CB.grid(row=10, column=3, columnspan=2, sticky=W, pady=3, padx=3)
		blank4_Label.grid(row=10, column=5, pady=3,padx=3)
		
		okButton.grid(row=11, column=0, columnspan=6, pady=3, padx=3)
		DocLabel_5.grid(row=12, column=0, columnspan=6, pady=3, padx=3)
		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		self.grid(row=0, column=0, sticky=NSEW)
		self.columnconfigure(1, weight=2)
		
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
$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 --dport {tcpport} -j ACCEPT'''
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
		out_if = ""
		out_ip4addr = ""
		out_ip4net = ""
		in_if = ""
		in_ip4addr = ""
		in_ip4net = ""
		serv022 = ""
		serv023 = ""
		serv993 = ""
		serv995 = ""
		serv873 = ""
		serv5900 = ""
		serv8080 = ""
		
		fmod = self.fmod_Var.get()
		out_if = self.out_if_Var.get()
		out_ip4addr = self.out_ip4addr_Var.get()
		out_ip4net = self.out_ip4net_Var.get()
		in_if = self.in_if_Var.get()
		in_ip4addr = self.in_ip4addr_Var.get()
		in_ip4net = self.in_ip4net_Var.get()
		serv022 = self.serv022_Var.get()
		serv023 = self.serv023_Var.get()
		serv993 = self.serv993_Var.get()
		serv995 = self.serv995_Var.get()
		serv873 = self.serv873_Var.get()
		serv5900 = self.serv5900_Var.get()
		serv8080 = self.serv8080_Var.get()
		
		fmod = fmod.strip()
		out_if = out_if.strip()
		out_ip4addr = out_ip4addr.strip()
		out_ip4net = out_ip4net.strip()
		in_if = in_if.strip()
		in_ip4addr = in_ip4addr.strip()
		in_ip4net = in_ip4net.strip()
		serv022 = serv022.strip()
		serv023 = serv023.strip()
		serv993 = serv993.strip()
		serv995 = serv995.strip()
		serv873 = serv873.strip()
		serv5900 = serv5900.strip()
		serv8080 = serv8080.strip()
		self.accpeted = True
		
		# data check 
		out_ip4net_a = out_ip4net.split("/")
		in_ip4net_a = in_ip4net.split("/")
		if fmod == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒指明要「全部放行」或「嚴格鎖埠」")
		elif out_if == "":
			isdataok = "F"
			showerror(title="資訊不足", message="對外網卡沒指定")
		elif out_ip4addr == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒填實體 IPv4 位址")
		elif self.chkipv4(out_ip4addr) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="公用 IPv4 網址不合理請檢查")
		elif out_ip4net == "":
			isdataok = "F"
			showerror(title="資訊不足", message="允許 SSH 連線網址一沒填")
		elif self.chkipv4(out_ip4net_a[0]) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="允許 SSH 連線網址一格式不合理請檢查")
		elif in_if == "":
			isdataok = "F"
			showerror(title="資訊不足", message="對內網卡沒指定")
		elif in_ip4addr == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒填虛擬 IPv4 位址")
		elif self.chkipv4(in_ip4addr) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="私有 IPv4 網址不合理請檢查")
		elif in_ip4net == "":
			isdataok = "F"
			showerror(title="資訊不足", message="允許 SSH 連線網址二沒填")
		elif self.chkipv4(in_ip4net_a[0]) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="允許 SSH 連線網址二格式不合理請檢查")
		
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
				self.CommonRules = self.CommonRules.format(**locals())
				self.CommonRules2 = self.CommonRules2.format(**locals())
				self.StrictRules = self.StrictRules + "\n\n# 預設政策\n$IPTABLES -A FORWARD -o $FW_IFACE -p tcp -s any/0 -j DROP\n"
				self.RcLocal = self.CommonRules + self.StrictRules + self.CommonRules2
			elif fmod == "loose":
				self.CommonRules = self.CommonRules.format(**locals())
				self.CommonRules2 = self.CommonRules2.format(**locals())
				self.RcLocal = self.CommonRules + self.CommonRules2
			self.RcLocal = self.RcLocal + "\n\n# 下面這一行切勿刪除\nexit 0"
			self.confw( "rc.local" , self.RcLocal )
			subprocess.check_call(["/bin/chmod", "+x", "rc.local"])
			showinfo( title="完工", message="防火牆設定檔已寫成 rc.local，請以 root 身份覆蓋 /etc/rc.local" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 330)
mY = int(scrY/2 - 200) - 60
strGeometry = "660x400+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("NAT 防火牆 rc.local 產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

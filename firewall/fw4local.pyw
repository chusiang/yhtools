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
		self.ip4_a1_Var = StringVar()
		self.ip4_a2_Var = StringVar()
		self.ip4_a3_Var = StringVar()
		self.ip4_a4_Var = StringVar()
		self.ip6_a1_Var = StringVar()
		self.serv021_Var = StringVar()
		self.serv022_Var = StringVar()
		self.serv023_Var = StringVar()
		self.serv3389_Var = StringVar()
		self.serv137_Var = StringVar()
		self.serv143_Var = StringVar()
		self.serv993_Var = StringVar()
		self.serv995_Var = StringVar()
		self.IPv4Rules = ""
		self.IPv6Rules = ""
		self.RcLocal = '''#! /bin/bash
#
# 本 Script 參考自 OLS3 (ols3@lxer.idv.tw)
# 本 Script 受 /etc/init.d/rc.local 控管，切勿刪除最後一行「exit 0」
# Ubuntu 10.x 及 Debian lenny 之後版本，直接以本檔覆蓋 /etc/rc.local 
# 執行 service rc.local start 套用新規列
#

IPTABLES="/sbin/iptables"
IP6TABLES="/sbin/ip6tables"

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

###-----------------------------------------------------###
# 設定 filter table 的預設政策
###-----------------------------------------------------###
$IPTABLES -P INPUT ACCEPT
$IPTABLES -P OUTPUT ACCEPT
$IPTABLES -P FORWARD ACCEPT

'''
		
		DocLabel_1 = Label(self, text="充許連線的網段或網址，至少一組，不足處請自行修改 rc.local ", bg='blue', fg='white', font=( None, 12), width=54)
		ip4_a1_Label = Label(self, text="IPv4_1(必):")
		ip4_a1_Entry = Entry(self, textvariable=self.ip4_a1_Var, width=25)
		ip4_a1_Entry.focus_set()
		ip4_a2_Label = Label(self, text="IPv4_2:")
		ip4_a2_Entry = Entry(self, textvariable=self.ip4_a2_Var, width=25)
		ip4_a3_Label = Label(self, text="IPv4_3:")
		ip4_a3_Entry = Entry(self, textvariable=self.ip4_a3_Var, width=25)
		ip4_a4_Label = Label(self, text="IPv4_4:")
		ip4_a4_Entry = Entry(self, textvariable=self.ip4_a4_Var, width=25)
		ip6_a1_Label = Label(self, text="IPv6_1（可不填）:")
		ip6_a1_Entry = Entry(self, textvariable=self.ip6_a1_Var, width=25)
		DocLabel_2 = Label(self, text="（單IP直接填，網段請使用 CIDR notation 方式標註, 例: 192.168.1.0／24 或 2001:288:75a6::/48）")
		
		DocLabel_3 = Label(self, text="   ")
		DocLabel_4 = Label(self, text="勾選要阻擋的服務，至少要一組", bg='blue', fg='white', font=( None, 12), width=54)
		serv021_CB = Checkbutton(self, text="FTP_21   ", variable=self.serv021_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv022_CB = Checkbutton(self, text="SSH_22   ", variable=self.serv022_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv023_CB = Checkbutton(self, text="telnet_23", variable=self.serv023_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv137_CB = Checkbutton(self, text="SAMBA_四埠", variable=self.serv137_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv3389_CB = Checkbutton(self, text="Xrdp_3389 ", variable=self.serv3389_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv143_CB = Checkbutton(self, text="IMAP_143 ", variable=self.serv143_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv993_CB = Checkbutton(self, text="POP3s_993", variable=self.serv993_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		serv995_CB = Checkbutton(self, text="IMAPs_995", variable=self.serv995_Var, onvalue="T", offvalue="F", width=15, anchor=W)
		
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_5 = Label(self, text="（按 Escape 鍵離開）")
		
		DocLabel_1.grid(row=0, column=0, columnspan=4, pady=3, padx=3, ipady=3, ipadx=3 )
		ip4_a1_Label.grid(row=1, column=0, sticky=E, pady=3, padx=3)
		ip4_a1_Entry.grid(row=1, column=1, columnspan=3, sticky=W, pady=3, padx=3)
		ip4_a2_Label.grid(row=2, column=0, sticky=E, pady=3, padx=3)
		ip4_a2_Entry.grid(row=2, column=1, columnspan=3, sticky=W, pady=3, padx=3)
		ip4_a3_Label.grid(row=3, column=0, sticky=E, pady=3, padx=3)
		ip4_a3_Entry.grid(row=3, column=1, columnspan=3, sticky=W, pady=3, padx=3)
		ip4_a4_Label.grid(row=4, column=0, sticky=E, pady=3, padx=3)
		ip4_a4_Entry.grid(row=4, column=1, columnspan=3, sticky=W, pady=3, padx=3)
		ip6_a1_Label.grid(row=5, column=0, sticky=E, pady=3, padx=3)
		ip6_a1_Entry.grid(row=5, column=1, columnspan=3, sticky=W, pady=3, padx=3)
		DocLabel_2.grid(row=6, column=0, columnspan=4, pady=3, padx=3)
		DocLabel_3.grid(row=7, column=0, columnspan=4, pady=3, padx=3)
		DocLabel_4.grid(row=8, column=0, columnspan=4, pady=3, padx=3, ipady=3, ipadx=3)
		serv021_CB.grid(row=9, column=0, sticky=E, pady=3, padx=8)
		serv022_CB.grid(row=9, column=1, sticky=E, pady=3, padx=8)
		serv023_CB.grid(row=9, column=2, sticky=E, pady=3, padx=8)
		serv137_CB.grid(row=9, column=3, sticky=E, pady=3, padx=8)
		serv3389_CB.grid(row=10, column=0, sticky=E, pady=3, padx=8)
		serv143_CB.grid(row=10, column=1, sticky=E, pady=3, padx=8)
		serv993_CB.grid(row=10, column=2, sticky=E, pady=3, padx=8)
		serv995_CB.grid(row=10, column=3, sticky=E, pady=3, padx=8)
		
		okButton.grid(row=11, column=0, columnspan=4, pady=3, padx=3)
		DocLabel_5.grid(row=12, column=0, columnspan=4, pady=3, padx=3)
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
		ip4_a1 = self.ip4_a1_Var.get()
		ip4_a2 = self.ip4_a2_Var.get()
		ip4_a3 = self.ip4_a3_Var.get()
		ip4_a4 = self.ip4_a4_Var.get()
		ip6_a1 = self.ip6_a1_Var.get()
		ip4_a1 = ip4_a1.strip()
		ip4_a2 = ip4_a2.strip()
		ip4_a3 = ip4_a3.strip()
		ip4_a4 = ip4_a4.strip()
		ip6_a1 = ip6_a1.strip()
		if tcpport != "137":
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a1+" --dport "+tcpport+" -j ACCEPT"
			if ip4_a2 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a2+" --dport "+tcpport+" -j ACCEPT"
			if ip4_a3 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a3+" --dport "+tcpport+" -j ACCEPT"
			if ip4_a4 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a4+" --dport "+tcpport+" -j ACCEPT"
			
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport "+tcpport+" -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp --dport "+tcpport+" -j DROP\n"
		else:
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a1+" --dport 139 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a1+" --dport 445 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a1+" --dport 137 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a1+" --dport 138 -j ACCEPT"
			if ip4_a2 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a2+" --dport 139 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a2+" --dport 445 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a2+" --dport 137 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a2+" --dport 138 -j ACCEPT"
			if ip4_a3 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a3+" --dport 139 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a3+" --dport 445 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a3+" --dport 137 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a3+" --dport 138 -j ACCEPT"
			if ip4_a3 != "":
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a4+" --dport 139 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s "+ip4_a4+" --dport 445 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a4+" --dport 137 -j ACCEPT"
				self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s "+ip4_a4+" --dport 138 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport 139 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp -s 127.0.0.1 --dport 445 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s 127.0.0.1 --dport 137 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp -s 127.0.0.1 --dport 138 -j ACCEPT"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp --dport 139 -j DROP"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p tcp --dport 445 -j DROP"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp --dport 137 -j DROP"
			self.IPv4Rules = self.IPv4Rules + "\n$IPTABLES -A INPUT -p udp --dport 138 -j DROP\n"
		if ip6_a1 != "":
			if tcpport != "137":
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s "+ip6_a1+" --dport "+tcpport+" -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s ::1 --dport "+tcpport+" -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp --dport "+tcpport+" -j DROP\n"
			else:
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s "+ip6_a1+" --dport 139 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s "+ip6_a1+" --dport 445 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp -s "+ip6_a1+" --dport 137 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp -s "+ip6_a1+" --dport 138 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s ::1 --dport 139 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp -s ::1 --dport 445 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp -s ::1 --dport 137 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp -s ::1 --dport 138 -j ACCEPT"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp --dport 139 -j DROP"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p tcp --dport 445 -j DROP"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp --dport 137 -j DROP"
				self.IPv6Rules = self.IPv6Rules + "\n$IP6TABLES -A INPUT -p udp --dport 138 -j DROP\n"
	
	def ok(self, event=None):
		isdataok = "T"
		ip4_a1 = ""
		ip4_a2 = ""
		ip4_a3 = ""
		ip4_a4 = ""
		ip6_a1 = ""
		serv021 = ""
		serv022 = ""
		serv023 = ""
		serv137 = ""
		serv3389 = ""
		serv143 = ""
		serv993 = ""
		serv995 = ""
		
		ip4_a1 = self.ip4_a1_Var.get()
		ip4_a2 = self.ip4_a2_Var.get()
		ip4_a3 = self.ip4_a3_Var.get()
		ip4_a4 = self.ip4_a4_Var.get()
		ip6_a1 = self.ip6_a1_Var.get()
		ip4_a1 = ip4_a1.strip()
		ip4_a2 = ip4_a2.strip()
		ip4_a3 = ip4_a3.strip()
		ip4_a4 = ip4_a4.strip()
		ip6_a1 = ip6_a1.strip()
		serv021 = self.serv021_Var.get()
		serv022 = self.serv022_Var.get()
		serv023 = self.serv023_Var.get()
		serv137 = self.serv137_Var.get()
		serv3389 = self.serv3389_Var.get()
		serv143 = self.serv143_Var.get()
		serv993 = self.serv993_Var.get()
		serv995 = self.serv995_Var.get()
		serv021 = serv021.strip()
		serv022 = serv022.strip()
		serv023 = serv023.strip()
		serv137 = serv137.strip()
		serv3389 = serv3389.strip()
		serv143 = serv143.strip()
		serv993 = serv993.strip()
		serv995 = serv995.strip()
		self.accpeted = True
		
		# data check 
		if ip4_a1 == "":
			isdataok = "F"
			showerror(title="資訊不足", message="第一筆允許連線網址沒填！")
		elif serv021 == "" and serv022 == "" and serv023 == "" and serv137 == "" and serv3389 == "" and serv143 == "" and serv993 == "" and serv995 == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒有任何服務是被勾選的！")
		
		if isdataok == "T":
			if serv021 == "T":
				self.createRules("21")
			if serv022 == "T":
				self.createRules("22")
			if serv023 == "T":
				self.createRules("23")
			if serv137 == "T":
				self.createRules("137")
			if serv3389 == "T":
				self.createRules("3389")
			if serv143 == "T":
				self.createRules("143")
			if serv993 == "T":
				self.createRules("993")
			if serv995 == "T":
				self.createRules("995")
			self.RcLocal = self.RcLocal + self.IPv4Rules + self.IPv6Rules
			self.RcLocal = self.RcLocal + "\n# 下面這一行切勿刪除\nexit 0"
			self.confw( "rc.local" , self.RcLocal )
			subprocess.check_call(["/bin/chmod", "+x", "rc.local"])
			showinfo( title="完工", message="防火牆設定檔已寫成 rc.local，請以 root 身份覆蓋原 /etc/rc.local" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 300)
mY = int(scrY/2 - 190) - 60
strGeometry = "600x380+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("本機防火牆規則列 rc.local 產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# License: GPL v2
# Language: zh_TW.utf8
# Version: 0.1.0
# Last modified: 2011-04-18
# Author: Y.H.Liu
import subprocess, os
from tkinter import *
from tkinter.messagebox import *

class MainWindow(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.fmod_Var = StringVar()
		self.dhcp_if_Var = StringVar()
		self.ip_start_Var = StringVar()
		self.ip_stop_Var = StringVar()
		self.dn_Var = StringVar()
		self.gateway_Var = StringVar()
		self.network_Var = StringVar()
		self.netmask_Var = StringVar()
		self.broadcast_Var = StringVar()
		self.dnsip_Var = StringVar()
		self.bind_ip_Var = [StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
		self.bind_mac_Var = [StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
		self.pnetwork_Var = StringVar()
		self.pnetmask_Var = StringVar()
		self.AllBinds = ""
		self.dhcp3_interfaces = '''# Defaults for dhcp initscript
# sourced by /etc/init.d/dhcp
# installed at /etc/default/isc-dhcp-server by the maintainer scripts

#
# This is a POSIX shell fragment
#

# On what interfaces should the DHCP server (dhcpd) serve DHCP requests?
#       Separate multiple interfaces with spaces, e.g. "eth0 eth1".
INTERFACES="{dhcp_if}"
'''
		
		self.dhcpd_conf = '''#
# Sample configuration file for ISC dhcpd for Debian
#
# Attention: If /etc/ltsp/dhcpd.conf exists, that will be used as
# configuration file instead of this file.
#
# $Id: dhcpd.conf,v 1.1.1.1 2002/05/21 00:07:44 peloy Exp $
#

# The ddns-updates-style parameter controls whether or not the server will
# attempt to do a DNS update when a lease is confirmed. We default to the
# behavior of the version 2 packages ('none', since DHCP v2 didn't
# have support for DDNS.)
ddns-update-style none;

# option definitions common to all supported networks...
option domain-name "{dn}";
#option domain-name-servers ns1.example.org, ns2.example.org;

default-lease-time 600;
max-lease-time 7200;

# This is a very basic subnet declaration.
subnet {network} netmask {netmask} {{
    range {ip_start} {ip_stop} ;
    option broadcast-address {broadcast} ;
    option routers {gateway} ;
    option domain-name-servers {dnsip} ;{allbinds}
}}
'''
		self.private_add = '''
# 若分配的是私有 IP, 需手動額外加入公用網段資料
subnet {pnetwork} netmask {pnetmask} {{

}}'''
		
		fmod_Label = Label(self, text="配送IP種類：",font=( None, 12), width=12, anchor=E)
		fmod1_RB = Radiobutton(self, text="公用IP(Public)", variable=self.fmod_Var, value="public", font=( None, 12))
		fmod2_RB = Radiobutton(self, text="私有IP(Private)", variable=self.fmod_Var, value="private", font=( None, 12))
		self.fmod_Var.set("private")
		blank1_Label = Label(self, text=" ", width=1)
		blank2_Label = Label(self, text="  ", width=1)
		DocLabel_1 = Label(self, text="基本設定", bg='blue', fg='white', font=( None, 12), width=62)
		dhcp_if_Label = Label(self, text="派送網卡(eth1):", width=12, anchor=E)
		dhcp_if_Entry = Entry(self, textvariable=self.dhcp_if_Var, width=15)
		self.dhcp_if_Var.set("eth1")
		dhcp_if_Entry.focus_set()
		ip_start_Label = Label(self, text="派送起始IP:", width=12, anchor=E)
		ip_start_Entry = Entry(self, textvariable=self.ip_start_Var, width=15)
		ip_stop_Label = Label(self, text="派送結束IP:", width=12, anchor=E)
		ip_stop_Entry = Entry(self, textvariable=self.ip_stop_Var, width=15)
		dn_Label = Label(self, text="網域名稱:", width=12, anchor=E)
		dn_Entry = Entry(self, textvariable=self.dn_Var, width=15)
		gateway_Label = Label(self, text="Gateway:", width=17, anchor=E)
		gateway_Entry = Entry(self, textvariable=self.gateway_Var, width=15)
		network_Label = Label(self, text="網段起始IP(例x.x.x.0):", width=17, anchor=E)
		network_Entry = Entry(self, textvariable=self.network_Var, width=15)
		self.netmask_Var.set("255.255.255.")
		netmask_Label = Label(self, text="網路遮罩:", width=17, anchor=E)
		netmask_Entry = Entry(self, textvariable=self.netmask_Var, width=15)
		broadcast_Label = Label(self, text="廣播位址(例x.x.x.255):", width=17, anchor=E)
		broadcast_Entry = Entry(self, textvariable= self.broadcast_Var, width=15)
		dnsip_Label = Label(self, text="指定DNS:", width=15, anchor=E)
		dnsip_Entry = Entry(self, textvariable=self.dnsip_Var, width=24)
		dnsipdoc_Label = Label(self, text="(例:163.26.182.1, 168.95.1.1)", anchor=W)
		DocLabel_blank = Label(self, text="   ")
		DocLabel_2 = Label(self, text="IP-MAC 鎖定派送設定", bg='blue', fg='white', font=( None, 12), width=62)
		doc_ip_Label = Label(self, text="IPv4位址")
		doc_mac_Label = Label(self, text="MAC位址")
		doc_ip2_Label = Label(self, text="IPv4位址")
		doc_mac2_Label = Label(self, text="MAC位址")
		bind_Label = [Label(self, text="1", width=2, anchor=E),Label(self, text="2", width=2,  anchor=E),
			Label(self, text="3", width=2, anchor=E),Label(self, text="4", width=2, anchor=E),
			Label(self, text="5", width=2, anchor=E),Label(self, text="6", width=2, anchor=E),
			Label(self, text="7", width=2, anchor=E),Label(self, text="8", width=2, anchor=E),
			Label(self, text="9", width=2, anchor=E),Label(self, text="10", width=2, anchor=E)]
		bind_ip_Entry = [Entry(self, textvariable=self.bind_ip_Var[0],width=15),Entry(self, textvariable=self.bind_ip_Var[1],width=15),
			Entry(self, textvariable=self.bind_ip_Var[2],width=15),Entry(self, textvariable=self.bind_ip_Var[3],width=15),
			Entry(self, textvariable=self.bind_ip_Var[4],width=15),Entry(self, textvariable=self.bind_ip_Var[5],width=15),
			Entry(self, textvariable=self.bind_ip_Var[6],width=15),Entry(self, textvariable=self.bind_ip_Var[7],width=15),
			Entry(self, textvariable=self.bind_ip_Var[8],width=15),Entry(self, textvariable=self.bind_ip_Var[9],width=15)]
		bind_mac_Entry = [Entry(self, textvariable=self.bind_mac_Var[0],width=15),Entry(self, textvariable=self.bind_mac_Var[1],width=15),
			Entry(self, textvariable=self.bind_mac_Var[2],width=15),Entry(self, textvariable=self.bind_mac_Var[3],width=15),
			Entry(self, textvariable=self.bind_mac_Var[4],width=15),Entry(self, textvariable=self.bind_mac_Var[5],width=15),
			Entry(self, textvariable=self.bind_mac_Var[6],width=15),Entry(self, textvariable=self.bind_mac_Var[7],width=15),
			Entry(self, textvariable=self.bind_mac_Var[8],width=15),Entry(self, textvariable=self.bind_mac_Var[9],width=15)]
		
		DocLabel_2b = Label(self, text="（預設只有十組，不足之處請修改產生的 dhcpd.conf 設定檔）")
		
		DocLabel_3 = Label(self, text="選「私有IP」者，必填項目", bg='blue', fg='white', font=( None, 12), width=62)
		pnetwork_Label = Label(self, text="公用網段起始IP:", anchor=E)
		pnetwork_Entry = Entry(self, textvariable=self.pnetwork_Var, width=15)
		self.pnetmask_Var.set("255.255.255.")
		pnetmask_Label = Label(self, text="公用網段遮罩:", anchor=E)
		pnetmask_Entry = Entry(self, textvariable=self.pnetmask_Var, width=15)
		pnetworkex_Label = Label(self, text="（例: 163.26.182.0）")
		pnetmaskex_Label = Label(self, text="（例: 255.255.255.0）")
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_6 = Label(self, text="（按 Escape 鍵離開）")
		
		blank1_Label.grid(row=0, column=0, pady=3, padx=1)
		fmod_Label.grid(row=0, column=1, sticky=E, pady=3, padx=3, ipady=3, ipadx=1)
		fmod1_RB.grid(row=0, column=2, columnspan=2, sticky=E, pady=3, padx=3, ipady=3, ipadx=3)
		fmod2_RB.grid(row=0, column=4, columnspan=3, sticky=W, pady=3, padx=3, ipady=3, ipadx=3)
		DocLabel_1.grid(row=1, column=0, columnspan=7, pady=3, padx=3, ipady=3, ipadx=3 )
		blank1_Label.grid(row=2, column=0, pady=3, padx=2)
		dhcp_if_Label.grid(row=2, column=1, sticky=E, pady=3, padx=3)
		dhcp_if_Entry.grid(row=2, column=2, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=2, column=3, pady=3, padx=1)
		gateway_Label.grid(row=2, column=4, sticky=E, pady=3, padx=3)
		gateway_Entry.grid(row=2, column=5, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=2, column=6, pady=3, padx=1)
		blank1_Label.grid(row=3, column=0, pady=3, padx=2)
		ip_start_Label.grid(row=3, column=1, sticky=E, pady=3, padx=3)
		ip_start_Entry.grid(row=3, column=2, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=3, column=3, pady=3, padx=1)
		network_Label.grid(row=3, column=4, sticky=E, pady=3, padx=3)
		network_Entry.grid(row=3, column=5, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=3, column=6, pady=3, padx=1)
		blank1_Label.grid(row=4, column=0, pady=3, padx=2)
		ip_stop_Label.grid(row=4, column=1, sticky=E, pady=3, padx=3)
		ip_stop_Entry.grid(row=4, column=2, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=4, column=3, pady=3, padx=1)
		netmask_Label.grid(row=4, column=4, sticky=E, pady=3, padx=3)
		netmask_Entry.grid(row=4, column=5, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=4, column=6, pady=3, padx=1)
		blank1_Label.grid(row=5, column=0, pady=3, padx=2)
		dn_Label.grid(row=5, column=1, sticky=E, pady=3, padx=3)
		dn_Entry.grid(row=5, column=2, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=5, column=3, pady=3, padx=1)
		broadcast_Label.grid(row=5, column=4, sticky=E, pady=3, padx=3)
		broadcast_Entry.grid(row=5, column=5, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=5, column=6, pady=3, padx=1)
		blank1_Label.grid(row=6, column=0, pady=3, padx=2)
		dnsip_Label.grid(row=6, column=1, stick=E, pady=3, padx=3)
		dnsip_Entry.grid(row=6, column=2, columnspan=2, sticky=W, pady=3, padx=3)
		dnsipdoc_Label.grid(row=6, column=4, columnspan=2, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=6, column=6, pady=3, padx=1)
		
		DocLabel_2.grid(row=7, column=0, columnspan=7, pady=3, padx=3)
		blank1_Label.grid(row=8, column=0, pady=3, padx=2)
		doc_ip_Label.grid(row=8, column=1, pady=3, padx=3)
		doc_mac_Label.grid(row=8, column=2, pady=3, padx=3)
		blank1_Label.grid(row=8, column=3, pady=3, padx=1)
		doc_ip2_Label.grid(row=8, column=4, pady=3, padx=3)
		doc_mac2_Label.grid(row=8, column=5, pady=3, padx=3)
		blank2_Label.grid(row=8, column=6, pady=3, padx=1)
		for i in range(5):
			nr = i + 9
			bind_Label[i].grid(row=nr, column=0, sticky=E, pady=3, padx=2)
			bind_ip_Entry[i].grid(row=nr, column=1, pady=3, padx=3)
			bind_mac_Entry[i].grid(row=nr, column=2, pady=3, padx=3)
			j = i + 5
			bind_Label[j].grid(row=nr, column=3, sticky=E, pady=3, padx=3)
			bind_ip_Entry[j].grid(row=nr, column=4, pady=3, padx=3)
			bind_mac_Entry[j].grid(row=nr, column=5, pady=3, padx=3)
			blank2_Label.grid(row=nr, column=6, pady=3, padx=1)
		
		DocLabel_3.grid(row=14, column=0, columnspan=7, pady=3, padx=3, ipady=3, ipadx=3 )
		blank1_Label.grid(row=15, column=0, pady=3, padx=2)
		pnetwork_Label.grid(row=15, column=1, sticky=E, pady=3, padx=3)
		pnetwork_Entry.grid(row=15, column=2, sticky=W, pady=3, padx=3)
		blank1_Label.grid(row=15, column=3, pady=3, padx=2)
		pnetmask_Label.grid(row=15, column=4, sticky=E, pady=3, padx=3)
		pnetmask_Entry.grid(row=15, column=5, sticky=W, pady=3, padx=3)
		blank2_Label.grid(row=15, column=6, pady=3, padx=1)
		blank1_Label.grid(row=16, column=0, pady=3, padx=2)
		pnetworkex_Label.grid(row=16, column=1, columnspan=2, pady=3, padx=3)
		blank1_Label.grid(row=16, column=3, pady=3, padx=2)
		pnetmaskex_Label.grid(row=16, column=4, columnspan=2, pady=3, padx=3)
		blank2_Label.grid(row=16, column=6, pady=3, padx=1)
		
		okButton.grid(row=17, column=0, columnspan=7, pady=3, padx=3)
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
	
	def createBind(self, ip4, mac):
		ip4_a = ip4.split(".")
		pcno = ip4_a[3]
		Binds = '''
    host pc{pcno} {{
        hardware ethernet {mac};
        fixed-address {ip4}; }}'''
		
		Binds = Binds.format(**locals())
		self.AllBinds = self.AllBinds + Binds
	
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
		dhcp_if = ""
		ip_start = ""
		ip_stop = ""
		dn = ""
		gateway = ""
		network = ""
		netmask = ""
		broadcast = ""
		dnsip = ""
		pnetwork = ""
		pnetmask= ""
		bind_ip = ["","","","","","","","","",""]
		bind_mac = ["","","","","","","","","",""]
		allbinds = ""
		
		fmod = self.fmod_Var.get()
		dhcp_if = self.dhcp_if_Var.get()
		ip_start = self.ip_start_Var.get()
		ip_stop = self.ip_stop_Var.get()
		dn = self.dn_Var.get()
		gateway = self.gateway_Var.get()
		network = self.network_Var.get()
		netmask = self.netmask_Var.get()
		broadcast = self.broadcast_Var.get()
		dnsip = self.dnsip_Var.get()
		pnetwork = self.pnetwork_Var.get()
		pnetmask= self.pnetmask_Var.get()
		for i in range(10):
			bind_ip[i] = self.bind_ip_Var[i].get()
			bind_mac[i] = self.bind_mac_Var[i].get()
				
		fmod = fmod.strip()
		dhcp_if = dhcp_if.strip()
		ip_start = ip_start.strip()
		ip_stop = ip_stop.strip()
		dn = dn.strip()
		gateway = gateway.strip()
		network = network.strip()
		netmask = netmask.strip()
		broadcast = broadcast.strip()
		dnsip = dnsip.strip()
		pnetwork = pnetwork.strip()
		pnetmask= pnetmask.strip()
		for i in range(10):
			bind_ip[i] = bind_ip[i].strip()
			bind_mac[i] = bind_mac[i].strip()
		self.accpeted = True
		
		# data check 
		if fmod == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒指明要「全部放行」或「嚴格鎖埠」")
		elif dhcp_if == "":
			isdataok = "F"
			showerror(title="資訊不足", message="派送IP網卡沒指定")
		elif ip_start == "":
			isdataok = "F"
			showerror(title="資訊不足", message="派送起始 IP 沒填")
		elif self.chkipv4(ip_start) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="派送起始 IP 不合理請檢查")
		elif ip_stop == "":
			isdataok = "F"
			showerror(title="資訊不足", message="派送結束 IP 沒填")
		elif self.chkipv4(ip_stop) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="派送結束 IP 不合理請檢查")
		elif gateway == "":
			isdataok = "F"
			showerror(title="資訊不足", message="Gateway 網址沒填")
		elif self.chkipv4(gateway) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="Gateway 網址格式不合理請檢查")
		elif network == "":
			isdataok = "F"
			showerror(title="資訊不足", message="網段起始位址沒填")
		elif self.chkipv4(network) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="網段起始位址格式不合理請檢查")
		elif netmask == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒填網路遮罩")
		elif self.chkipv4(netmask) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="網路遮罩寫法不合理請檢查")
		elif broadcast == "":
			isdataok = "F"
			showerror(title="資訊不足", message="沒填「網路廣播」位址")
		elif self.chkipv4(broadcast) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="「網路廣播」位址寫法不合理請檢查")
		elif dnsip == "":
			isdataok = "F"
			showerror(title="資訊不足", message="指定 DNS 沒填")
		elif fmod == "private" and pnetwork=="":
			isdataok = "F"
			showerror(title="錯誤", message="您選了「私有IP配送」，但沒填「公用網段起始IP」")
		elif fmod == "private" and pnetmask=="":
			isdataok = "F"
			showerror(title="錯誤", message="您選了「私有IP配送」，但沒填「公用網段遮罩」")
		elif fmod == "private" and self.chkipv4(pnetmask) == "F":
			isdataok = "F"
			showerror(title="錯誤", message="「公用網路遮罩」寫法不合理請檢查")
		
		if isdataok == "T":
			for i in range(10):
				if bind_ip[i] != "" and bind_mac[i] != "":
					self.createBind(bind_ip[i], bind_mac[i])
			self.dhcp3_interfaces = self.dhcp3_interfaces.format(**locals())
			self.confw( "isc-dhcp-server" , self.dhcp3_interfaces )
			allbinds = self.AllBinds
			#print( allbinds )
			self.dhcpd_conf = self.dhcpd_conf.format(**locals())
			if fmod == "private":
				self.private_add = self.private_add.format(**locals())
				self.dhcpd_conf = self.dhcpd_conf + self.private_add
			self.confw( "dhcpd.conf", self.dhcpd_conf )
			
			showinfo( title="完工", message="isc-dhcp-server 放到/etc/default/;  dhcpd.conf 放在 /etc/dhcp" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 325)
mY = int(scrY/2 - 263) - 20
strGeometry = "650x526+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("DHCP 設定檔產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

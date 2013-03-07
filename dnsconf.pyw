#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# License: GPL v2
# Language: zh_TW.utf8
# Version: 0.3.1
# Last modified: 2011-03-29
# Author: YungHusan Roger Liu
import subprocess, os
from tkinter import *
from tkinter.messagebox import *
import time
from datetime import date

class MainWindow(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.zonenameVar = StringVar()
		self.ip4_dnsipVar = StringVar()
		self.ip4_revVar = StringVar()
		self.ip6_networkVar = StringVar()
		self.ip6_dnsipVar = StringVar()
		self.ns_recurVar = StringVar()
		
		zonenameLabel = Label(self, text="網域名稱(必填):")
		zonenameEntry = Entry(self, textvariable=self.zonenameVar)
		zonenameEntry.focus_set()
		ip4_dnsipLabel = Label(self, text="DNS IPv4 位址(必填):")
		ip4_dnsipEntry = Entry(self, textvariable=self.ip4_dnsipVar)
		ip4_revVarLabel = Label(self, text="產生 IPv4 反解?")
		ip4_revVarCB = Checkbutton(self, variable=self.ip4_revVar, onvalue="T", offvalue="F")
		ip6_networkLabel = Label(self, text="IPv6 網段(ex. \"2001:288:22\") :")
		ip6_networkEntry = Entry(self, textvariable=self.ip6_networkVar)
		ip6_dnsipLabel = Label(self, text="DNS IPv6 位址(ex. \"1\") :")
		ip6_dnsipEntry = Entry(self, textvariable=self.ip6_dnsipVar)
		ip6_exLabel = Label(self, text="(依上例 IPv6 位址將會被組合成: 2001:288:22::1)")
		ns_recurLabel = Label(self, text="是否限制遞迴查詢?")
		ns_recurCB = Checkbutton(self, variable=self.ns_recurVar, onvalue="T", offvalue="F")
		okButton = Button(self, text="確定", command=self.ok)
		escape_docLabel = Label(self, text="(按 Escape 鍵離開)")
		
		zonenameLabel.grid(row=0, column=0, sticky=W, pady=3, padx=3)
		zonenameEntry.grid(row=0, column=1, sticky=EW, pady=3, padx=3)
		ip4_dnsipLabel.grid(row=1, column=0, sticky=W, pady=3, padx=3)
		ip4_dnsipEntry.grid(row=1, column=1, sticky=EW, pady=3, padx=3)
		ip4_revVarLabel.grid(row=2, column=0, sticky=W, pady=3, padx=3)
		ip4_revVarCB.grid(row=2, column=1, sticky=W, pady=3, padx=3)
		ip6_networkLabel.grid(row=3, column=0, sticky=W, pady=3, padx=3)
		ip6_networkEntry.grid(row=3, column=1, sticky=EW, pady=3, padx=3)
		ip6_dnsipLabel.grid(row=4, column=0, sticky=W, pady=3, padx=3)
		ip6_dnsipEntry.grid(row=4, column=1, sticky=EW, pady=3, padx=3)
		ip6_exLabel.grid(row=5, column=0, columnspan=2, pady=3, padx=3)
		ns_recurLabel.grid(row=6, column=0, sticky=W, pady=3, padx=3)
		ns_recurCB.grid(row=6, column=1, sticky=W, pady=3, padx=3)
		okButton.grid(row=7, column=0, columnspan=2, pady=3, padx=3)
		escape_docLabel.grid(row=8, column=0, columnspan=2, pady=3, padx=3)
		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		self.grid(row=0, column=0, sticky=NSEW)
		self.columnconfigure(1, weight=2)
		
		self.master.bind("<Return>", self.ok)
		self.master.bind("<Escape>", self.close)
		
	
	def confw(self, fname, fcontent):
		fname = "./dnsconf/" + fname
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

	def ok(self, event=None):
		isdataok = "T"
		zonename = ""
		ip4_dnsip = ""
		ip4_rev = ""
		ip6_network = ""
		ip6_dnsip = ""
		ns_recur = ""
		td = ""
		tdsn = ""

		NamedConf = '''// This is the primary configuration file for the BIND DNS server named.
//
// Please read /usr/share/doc/bind9/README.Debian.gz for information on the 
// structure of BIND configuration files in Debian, *BEFORE* you customize 
// this configuration file.
//
// If you are just adding zones, please do that in /etc/bind/named.conf.local

include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
'''

		NamedConfLocal = '''//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";

include "/etc/bind/named.conf.default-zones";

zone "{zonename}" {{
	type master;
	file "/etc/bind/db.{zonename}";
}};

{ip4_reverse}

{ip6_reverse}
'''

		NamedConfNsRecur = '''//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";

// 把學校 IPv6 網段加入可允許查詢區，例：新增 2001:288:75a6::/48;
acl allow_clients {{ 127.0.0.1; {ip4_netblock} {ip6_netblock} }};

// 在 acl 中的 IP 允許的操作
view "recursive" {{
     match-clients {{ allow_clients; }};
     recursion yes;
     include "/etc/bind/auth_zones.conf";
}};

// 未在 acl 中的 IP 拒絕使用遞迴式查詢
view "external" {{
     match-clients {{ any; }};
     recursion no;
     include "/etc/bind/auth_zones.conf";
}}; 
'''
		AuthZones = '''include "/etc/bind/named.conf.default-zones";

zone "{zonename}" {{
	type master;
	file "/etc/bind/db.{zonename}";
}};

{ip4_reverse}

{ip6_reverse}
'''

		ZoneContent = '''$TTL 86400
@	IN	SOA	dns.{zonename}.	admin.dns.{zonename}. (
			{tdsn}	; serial
			86400		; refresh
			1800		; retry
			1728000 	; expire
			1200    	; Negative Caching
			)
      IN	NS	dns.{zonename}.
dns		IN	A	{ip4_dnsip}
{ip6_dnsip2}
@		IN	MX	10	mail.{zonename}.
{zonename}. 	IN 	A 	{ip4_dnsip}
{ip6_dnsip2}
;
www   IN	CNAME	dns.{zonename}.
ftp   IN	CNAME	dns.{zonename}.
;
mail	IN	A	{ip4_dnsip}
{ip6_dnsip2}
'''

		IP4Reverse = '''
zone "{ip4_first3_reverse}.in-addr.arpa" {{
	type master;
	file "/etc/bind/db.{ip4_first3}";
}};
'''

		IP4RevContent = '''$TTL 86400
@	IN	SOA	dns.{zonename}.	admin.dns.{zonename}. (
			{tdsn}	; serial
			86400 		; refresh
			1800 		; retry
			1728000 	; expire
			1200    	; Negative Caching
			)
      IN	NS	dns.{zonename}.
;
{ip4_last}     IN	PTR	dns.{zonename}.
'''

		IP6Reverse = '''
// ::1 的反解檔
zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa."{{
        type master;
        file "/etc/bind/rev.local6";
}};

// IPv6 的反解檔
zone "{ip6_rtype1}ip6.arpa." {{
        type master;
        file "/etc/bind/{ip6_rtype2}rev";
}};
'''

		IP6RevLocal = '''$TTL 86400
@ IN    SOA dns.{zonename}. admin.dns.{zonename}. (1 15m 5m 30d 1h)
        IN      NS dns.{zonename}.
;;
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa. IN PTR localhost.
'''

		IP6RevZone = '''$TTL 86400
$ORIGIN {ip6_rtype1}ip6.arpa.
@ IN    SOA dns.{zonename}. admin.dns.{zonename}. (1 15m 5m 30d 1h)
        IN      NS dns.{zonename}.
;;
1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0 IN PTR dns.{zonename}.

'''
		td = date.today()
		tdsn = td.strftime("%Y%m%d")+"01"
		zonename = self.zonenameVar.get()
		ip4_dnsip = self.ip4_dnsipVar.get()
		ip4_rev = self.ip4_revVar.get()
		ip6_network = self.ip6_networkVar.get()
		ip6_dnsip = self.ip6_dnsipVar.get()
		ns_recur = self.ns_recurVar.get()
		self.accpeted = True
		
		if ip4_dnsip != "":
			ip4_list = ip4_dnsip.split(".")
		
		if ip4_dnsip == "":
			showerror(title="資訊不足", message="DNS IPv4 位址沒填!")
			isdataok = "F"
		elif not os.path.isdir("./dnsconf"):
			showerror(title="錯誤", message="找不到 ./dnsconf 資料夾，請重新下載 yhtools !")
			isdataok = "F"
		elif zonename == "":
			showerror(title="資訊不足", message="網域名稱沒填!")
			isdataok = "F"
		elif ip4_rev == "":
			showerror(title="資訊不足", message="請決定是否「產生 IPv4 反解」?")
			isdataok = "F"
		elif len(ip4_list) != 4:
			showerror(title="資訊不足", message="DNS IPv4 位址有誤!")
			isdataok = "F"	
		elif ip6_network != "":
			if ip6_dnsip == "":
				showerror(title="資訊不足", message="有 IPv6 網段，卻沒有 IPv6 位址!")
				isdataok = "F"
		elif ns_recur == "":
			showerror(title="資訊不足", message="請決定是否要「限制遞迴查詢」")
			isdataok = "F"

		if isdataok == "T":
			ip4_first3 = ip4_list[0] + "." + ip4_list[1] + "." + ip4_list[2]
			ip4_netblock = ip4_first3 + ".0/24;"
			ip4_last = ip4_list[3]
			if ip4_rev == "T":
				ip4_first3_reverse = ip4_list[2] + "." + ip4_list[1] + "." + ip4_list[0]
				ip4_reverse = IP4Reverse.format(**locals())
				fname = "db." + ip4_first3
				IP4RevContent = IP4RevContent.format(**locals())
				self.confw( fname, IP4RevContent )
			else:
				ip4_reverse = ""
			
			if ip6_network != "":
				ip6_rtype2 = ""
				ip6_list = ip6_network.split(":")
				if( len(ip6_list) == 3 ):
					ip6_netblock = ip6_network + "::/48;"
				elif( len(ip6_list) == 4 ):
					ip6_netblock = ip6_network + "::/64;"
				else:
					ip6_netblock = ""
				
				for i in range(len(ip6_list)):
					ip6_rtype2 = ip6_rtype2 + ip6_list[i] + "."
					ip6_list[i] = "{:0>4}".format(ip6_list[i])
				
				ip6_rtype1 = ""
				k = len(ip6_list) - 1
				for i in range(len(ip6_list)):
					j = k - i
					for iw in range(4):
						jw = 3 - iw
						ip6_rtype1 = ip6_rtype1 + ip6_list[j][jw] + "."
				ip6_dnsip = ip6_network + "::" + ip6_dnsip
				ip6_reverse = IP6Reverse.format(**locals())
				fname = "rev.local6"
				IP6RevLocal = IP6RevLocal.format(**locals())
				self.confw( fname, IP6RevLocal )
				fname = ip6_rtype2 + "rev"
				IP6RevZone = IP6RevZone.format(**locals())
				self.confw( fname, IP6RevZone )
				ip6_dnsip2 = "		IN	AAAA	" + ip6_dnsip
			else:
				ip6_reverse = ""
				ip6_dnsip == ""
				ip6_dnsip2 = ";"
			
			if ns_recur == "T" :
				NamedConfNsRecur = NamedConfNsRecur.format( **locals() )
				self.confw( "named.conf.local", NamedConfNsRecur )
				AuthZones = AuthZones.format( **locals() )
				self.confw( "auth_zones.conf", AuthZones )
			else:
				NamedConfLocal = NamedConfLocal.format( **locals() )
				self.confw( "named.conf.local", NamedConfLocal )
				
			zone_content = ZoneContent.format( **locals() )
			zonedbname = "db." + zonename
			self.confw( zonedbname, zone_content )
			self.confw( "named.conf" , NamedConf )
			showinfo( title="完工", message="設定檔已在 ./dnsconf 資料夾內，請自行複製到 /etc/bind" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 225)
mY = int(scrY/2 - 130) - 100
strGeometry = "450x260+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("DNS設定檔產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# License: GPL v2
# Language: zh_TW.utf8
# Version: 0.1.1
# Last modified: 2011-04-25
# Author: Y.H.Liu
import subprocess, os
from tkinter import *
from tkinter.messagebox import *

class MainWindow(Frame):
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.bkuser_id_Var = StringVar()
		self.bkuser_pwd_Var = StringVar()
		self.rsynsvr_ip_Var = StringVar()
		self.secname_Var = StringVar()
		self.bkpath01_Var = StringVar()
		self.bkpath02_Var = StringVar()
		self.bkpath03_Var = StringVar()
		self.bkpath04_Var = StringVar()
		self.bkpath05_Var = StringVar()
		self.bkpath06_Var = StringVar()
		self.bkpath07_Var = StringVar()
		self.bkpath08_Var = StringVar()
		self.bkpath09_Var = StringVar()
		self.bkpath10_Var = StringVar()
		
		self.rSyncbkSH = "#! /bin/bash\n"
		
		DocLabel_1 = Label(self, text="請以 root 身份執行", bg='blue', fg='white', font=( None, 12), width=58)
		bkuser_id_Label = Label(self, text="BKUser ID:", width=18, anchor=E)
		bkuser_id_Entry = Entry(self, textvariable=self.bkuser_id_Var, width=18)
		bkuser_id_Entry.focus_set()
		self.bkuser_id_Var.set("rsynbk")
		bkuser_pwd_Label = Label(self, text="BKUser 密碼:", width=14, anchor=E)
		bkuser_pwd_Entry = Entry(self, textvariable=self.bkuser_pwd_Var, width=18)
		rsynsvr_ip_Label = Label(self, text="rSyn伺服器IP位址:", width=18, anchor=E)
		rsynsvr_ip_Entry = Entry(self, textvariable=self.rsynsvr_ip_Var, width=18)
		secname_Label = Label(self, text="區段名稱:", width=14, anchor=E)
		secname_Entry = Entry(self, textvariable=self.secname_Var, width=18)
		DocLabel_2 = Label(self, text=" ")
		bkpath01_Label = Label(self, text="備份資料夾01:", width=18, anchor=E)
		bkpath01_Entry = Entry(self, textvariable=self.bkpath01_Var, width=18)
		self.bkpath01_Var.set("/etc")
		bkpath02_Label = Label(self, text="備份資料夾02:", width=18, anchor=E)
		bkpath02_Entry = Entry(self, textvariable=self.bkpath02_Var, width=18)
		self.bkpath02_Var.set("/home")
		bkpath03_Label = Label(self, text="備份資料夾03:", width=18, anchor=E)
		bkpath03_Entry = Entry(self, textvariable=self.bkpath03_Var, width=18)
		self.bkpath03_Var.set("/var/www")
		bkpath04_Label = Label(self, text="備份資料夾04:", width=18, anchor=E)
		bkpath04_Entry = Entry(self, textvariable=self.bkpath04_Var, width=18)
		self.bkpath04_Var.set("/var/lib/mysql")
		bkpath05_Label = Label(self, text="備份資料夾05:", width=18, anchor=E)
		bkpath05_Entry = Entry(self, textvariable=self.bkpath05_Var, width=18)
		self.bkpath05_Var.set("/usr/share")
		bkpath06_Label = Label(self, text="備份資料夾06:", width=14, anchor=E)
		bkpath06_Entry = Entry(self, textvariable=self.bkpath06_Var, width=18)
		bkpath07_Label = Label(self, text="備份資料夾07:", width=14, anchor=E)
		bkpath07_Entry = Entry(self, textvariable=self.bkpath07_Var, width=18)
		bkpath08_Label = Label(self, text="備份資料夾08:", width=14, anchor=E)
		bkpath08_Entry = Entry(self, textvariable=self.bkpath08_Var, width=18)
		bkpath09_Label = Label(self, text="備份資料夾09:", width=14, anchor=E)
		bkpath09_Entry = Entry(self, textvariable=self.bkpath09_Var, width=18)
		bkpath10_Label = Label(self, text="備份資料夾10:", width=14, anchor=E)
		bkpath10_Entry = Entry(self, textvariable=self.bkpath10_Var, width=18)
		DocLabel_3 = Label(self, text="（資料夾位置後面不可以再加「／」）")
		DocLabel_4 = Label(self, text=" ")
		blankL_Label = Label(self, text=" ", width=2)
		blankM_Label = Label(self, text=" ", width=2)
		blankR_Label = Label(self, text=" ", width=2)
		
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_5 = Label(self, text="（按 Escape 鍵離開）")
		
		DocLabel_1.grid(row=0, column=0, columnspan=7, pady=3, padx=3, ipady=3, ipadx=3 )
		blankL_Label.grid(row=1, column=0, pady=3, padx=3 )
		bkuser_id_Label.grid(row=1, column=1, sticky=E, pady=3, padx=3)
		bkuser_id_Entry.grid(row=1, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=1, column=3, pady=3, padx=3 )
		bkuser_pwd_Label.grid(row=1, column=4, sticky=E, pady=3, padx=3)
		bkuser_pwd_Entry.grid(row=1, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=1, column=6, pady=3, padx=3 )
		blankL_Label.grid(row=2, column=0, pady=3, padx=3 )
		rsynsvr_ip_Label.grid(row=2, column=1, sticky=E, pady=3, padx=3)
		rsynsvr_ip_Entry.grid(row=2, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=2, column=3, pady=3, padx=3 )
		secname_Label.grid(row=2, column=4, sticky=E, pady=3, padx=3)
		secname_Entry.grid(row=2, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=2, column=6, pady=3, padx=3 )
		
		DocLabel_2.grid(row=3, column=0, columnspan=7, pady=3, padx=3, ipady=3, ipadx=3 )
		blankL_Label.grid(row=4, column=0, pady=3, padx=3 )
		bkpath01_Label.grid(row=4, column=1, sticky=E, pady=3, padx=3)
		bkpath01_Entry.grid(row=4, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=4, column=3, pady=3, padx=3 )
		bkpath06_Label.grid(row=4, column=4, sticky=E, pady=3, padx=3)
		bkpath06_Entry.grid(row=4, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=4, column=6, pady=3, padx=3 )
		blankL_Label.grid(row=5, column=0, pady=3, padx=3 )
		bkpath02_Label.grid(row=5, column=1, sticky=E, pady=3, padx=3)
		bkpath02_Entry.grid(row=5, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=5, column=3, pady=3, padx=3 )
		bkpath07_Label.grid(row=5, column=4, sticky=E, pady=3, padx=3)
		bkpath07_Entry.grid(row=5, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=5, column=6, pady=3, padx=3 )
		blankL_Label.grid(row=6, column=0, pady=3, padx=3 )
		bkpath03_Label.grid(row=6, column=1, sticky=E, pady=3, padx=3)
		bkpath03_Entry.grid(row=6, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=6, column=3, pady=3, padx=3 )
		bkpath08_Label.grid(row=6, column=4, sticky=E, pady=3, padx=3)
		bkpath08_Entry.grid(row=6, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=6, column=6, pady=3, padx=3 )
		blankL_Label.grid(row=7, column=0, pady=3, padx=3 )
		bkpath04_Label.grid(row=7, column=1, sticky=E, pady=3, padx=3)
		bkpath04_Entry.grid(row=7, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=7, column=3, pady=3, padx=3 )
		bkpath09_Label.grid(row=7, column=4, sticky=E, pady=3, padx=3)
		bkpath09_Entry.grid(row=7, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=7, column=6, pady=3, padx=3 )
		blankL_Label.grid(row=8, column=0, pady=3, padx=3 )
		bkpath05_Label.grid(row=8, column=1, sticky=E, pady=3, padx=3)
		bkpath05_Entry.grid(row=8, column=2, sticky=W, pady=3, padx=3)
		blankM_Label.grid(row=8, column=3, pady=3, padx=3 )
		bkpath10_Label.grid(row=8, column=4, sticky=E, pady=3, padx=3)
		bkpath10_Entry.grid(row=8, column=5, sticky=W, pady=3, padx=3)
		blankR_Label.grid(row=8, column=6, pady=3, padx=3 )
		DocLabel_3.grid(row=9, column=0, columnspan=7, pady=3, padx=3)
		DocLabel_4.grid(row=10, column=0, columnspan=7, pady=3, padx=3)
		
		okButton.grid(row=11, column=0, columnspan=7, pady=3, padx=3)
		DocLabel_5.grid(row=12, column=0, columnspan=7, pady=3, padx=3)
		top = self.winfo_toplevel()
		top.columnconfigure(0, weight=1)
		self.grid(row=0, column=0, sticky=NSEW)
		self.columnconfigure(1, weight=2)
		
		self.master.bind("<Return>", self.ok)
		self.master.bind("<Escape>", self.close)
		
	
	def confw(self, fname, fcontent):
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
	
	def createBK(self, bkpath, bkuser_id, rsynsvr_ip, secname):
		ubk = "\n/usr/bin/rsync -rvlHpogDtS --password-file=/root/rsyncd.secrets {bkpath} {bkuser_id}@{rsynsvr_ip}::{secname}"
		ubk = ubk.format(**locals())
		self.rSyncbkSH = self.rSyncbkSH + ubk
	
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
		rSyncdSecrets = ""
		crond = ""
		bkuser_id = ""
		bkuser_pwd = ""
		rsynsvr_ip = ""
		secname = ""
		bkpath01 = ""
		bkpath02 = ""
		bkpath03 = ""
		bkpath04 = ""
		bkpath05 = ""
		bkpath06 = ""
		bkpath07 = ""
		bkpath08 = ""
		bkpath09 = ""
		bkpath10 = ""
		
		createCron = '''#! /bin/bash
echo "5 2 * * * /root/rsyncbk.sh" >> /var/spool/cron/crontabs/root'''
		
		bkuser_id = self.bkuser_id_Var.get()
		bkuser_pwd = self.bkuser_pwd_Var.get()
		rsynsvr_ip = self.rsynsvr_ip_Var.get()
		secname = self.secname_Var.get()
		bkpath01 = self.bkpath01_Var.get()
		bkpath02 = self.bkpath02_Var.get()
		bkpath03 = self.bkpath03_Var.get()
		bkpath04 = self.bkpath04_Var.get()
		bkpath05 = self.bkpath05_Var.get()
		bkpath06 = self.bkpath06_Var.get()
		bkpath07 = self.bkpath07_Var.get()
		bkpath08 = self.bkpath08_Var.get()
		bkpath09 = self.bkpath09_Var.get()
		bkpath10 = self.bkpath10_Var.get()
				
		bkuser_id = bkuser_id.strip()
		bkuser_pwd = bkuser_pwd.strip()
		rsynsvr_ip = rsynsvr_ip.strip()
		secname = secname.strip()
		bkpath01 = bkpath01.strip()
		bkpath02 = bkpath02.strip()
		bkpath03 = bkpath03.strip()
		bkpath04 = bkpath04.strip()
		bkpath05 = bkpath05.strip()
		bkpath06 = bkpath06.strip()
		bkpath07 = bkpath07.strip()
		bkpath08 = bkpath08.strip()
		bkpath09 = bkpath09.strip()
		bkpath10 = bkpath10.strip()
		self.accpeted = True
		
		# data check 
		if bkuser_id == "":
			isdataok = "F"
			showerror(title="資訊不足", message="BKUser ID 沒填！")
		elif bkuser_pwd == "":
			isdataok = "F"
			showerror(title="資訊不足", message="BKUser 密碼沒填")
		elif rsynsvr_ip == "":
			isdataok = "F"
			showerror(title="資訊不足", message="rsync伺服器IP沒填")
		elif self.chkipv4(rsynsvr_ip) == "F":
			isdataok = "F"
			showerror(title="IP格式有誤", message="rsync伺服器IP格式有誤")
		elif secname == "":
			isdataok = "F"
			showerror(title="資訊不足", message="區段名稱沒填")
		elif bkpath01 == "":
			isdataok = "F"
			showerror(title="資訊不足", message="至少要有一個備份路徑")
		
		if isdataok == "T":
			self.createBK( bkpath01, bkuser_id, rsynsvr_ip, secname )
			if bkpath02 != "":
				self.createBK( bkpath02, bkuser_id, rsynsvr_ip, secname )
			if bkpath03 != "":
				self.createBK( bkpath03, bkuser_id, rsynsvr_ip, secname )
			if bkpath04 != "":
				self.createBK( bkpath04, bkuser_id, rsynsvr_ip, secname )
			if bkpath05 != "":
				self.createBK( bkpath05, bkuser_id, rsynsvr_ip, secname )
			if bkpath06 != "":
				self.createBK( bkpath06, bkuser_id, rsynsvr_ip, secname )
			if bkpath07 != "":
				self.createBK( bkpath07, bkuser_id, rsynsvr_ip, secname )
			if bkpath08 != "":
				self.createBK( bkpath08, bkuser_id, rsynsvr_ip, secname )
			if bkpath09 != "":
				self.createBK( bkpath09, bkuser_id, rsynsvr_ip, secname )
			if bkpath10 != "":
				self.createBK( bkpath10, bkuser_id, rsynsvr_ip, secname )
			rSyncdSecrets = bkuser_pwd
			self.confw( "/root/rsyncd.secrets", rSyncdSecrets )
			self.confw( "/root/rsyncbk.sh" , self.rSyncbkSH )
			self.confw( "/root/createcron.sh", createCron )
			subprocess.check_call(["/bin/chmod", "+x", "/root/createcron.sh"])
			subprocess.check_call(["/root/createcron.sh"])
			subprocess.check_call(["/bin/rm", "-f", "/root/createcron.sh"])
			subprocess.check_call(["/bin/chmod", "400", "/root/rsyncd.secrets"])
			subprocess.check_call(["/bin/chmod", "+x", "/root/rsyncbk.sh"])
			showinfo( title="完工", message="已產生 /root/rsyncbk.sh ,並請用 crontab -e 修改定時備份排程" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 320)
mY = int(scrY/2 - 185) - 60
strGeometry = "640x370+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("rSync Client 產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

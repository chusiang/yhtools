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
		self.sec1name_Var = StringVar()
		self.sec2name_Var = StringVar()
		self.sec3name_Var = StringVar()
		self.rSyncdConf = "log file = /var/log/rsyncd.log\n"
		self.EtcDefaultRsync = '''# defaults file for rsync daemon mode

# start rsync in daemon mode from init.d script?
#  only allowed values are "true", "false", and "inetd"
#  Use "inetd" if you want to start the rsyncd from inetd,
#  all this does is prevent the init.d script from printing a message
#  about not starting rsyncd (you still need to modify inetd's config yourself).
RSYNC_ENABLE=true

# which file should be used as the configuration file for rsync.
# This file is used instead of the default /etc/rsyncd.conf
# Warning: This option has no effect if the daemon is accessed
#          using a remote shell. When using a different file for
#          rsync you might want to symlink /etc/rsyncd.conf to
#          that file.
# RSYNC_CONFIG_FILE=

# what extra options to give rsync --daemon?
#  that excludes the --daemon; that's always done in the init.d script
#  Possibilities are:
#   --address=123.45.67.89              (bind to a specific IP address)
#   --port=8730                         (bind to specified port; default 873)
RSYNC_OPTS=''

# run rsyncd at a nice level?
#  the rsync daemon can impact performance due to much I/O and CPU usage,
#  so you may want to run it at a nicer priority than the default priority.
#  Allowed values are 0 - 19 inclusive; 10 is a reasonable value.
RSYNC_NICE=''

# run rsyncd with ionice?
#  "ionice" does for IO load what "nice" does for CPU load.
#  As rsync is often used for backups which aren't all that time-critical,
#  reducing the rsync IO priority will benefit the rest of the system.
#  See the manpage for ionice for allowed options.
#  -c3 is recommended, this will run rsync IO at "idle" priority. Uncomment
#  the next line to activate this.
# RSYNC_IONICE='-c3'
'''
		
		DocLabel_1 = Label(self, text="請以 root 身份執行", bg='blue', fg='white', font=( None, 12), width=36)
		bkuser_id_Label = Label(self, text="BKUser ID:", width=22, anchor=E)
		bkuser_id_Entry = Entry(self, textvariable=self.bkuser_id_Var, width=18)
		bkuser_id_Entry.focus_set()
		self.bkuser_id_Var.set("rsynbk")
		bkuser_pwd_Label = Label(self, text="BKUser 密碼:", width=22, anchor=E)
		bkuser_pwd_Entry = Entry(self, textvariable=self.bkuser_pwd_Var, width=18)
		sec1name_Label = Label(self, text="區段一名稱(必):", width=22, anchor=E)
		sec1name_Entry = Entry(self, textvariable=self.sec1name_Var, width=18)
		self.sec1name_Var.set("bk1")
		sec2name_Label = Label(self, text="區段二名稱:", width=22, anchor=E)
		sec2name_Entry = Entry(self, textvariable=self.sec2name_Var, width=18)
		sec3name_Label = Label(self, text="區段三名稱:", width=22, anchor=E)
		sec3name_Entry = Entry(self, textvariable=self.sec3name_Var, width=18)
		DocLabel_2 = Label(self, text="（區段名稱請以英文命名；各區段儲存位置在「/mybk/區段名」底下）")
		DocLabel_3 = Label(self, text="（每區段可提供一組備份，三段全填，可提供三台主機之備份需求）")
		DocLabel_4 = Label(self, text=" ")
		
		okButton = Button(self, text="確定", command=self.ok)
		DocLabel_5 = Label(self, text="（按 Escape 鍵離開）")
		
		DocLabel_1.grid(row=0, column=0, columnspan=2, pady=3, padx=3, ipady=3, ipadx=3 )
		bkuser_id_Label.grid(row=1, column=0, sticky=E, pady=3, padx=3)
		bkuser_id_Entry.grid(row=1, column=1, sticky=W, pady=3, padx=3)
		bkuser_pwd_Label.grid(row=2, column=0, sticky=E, pady=3, padx=3)
		bkuser_pwd_Entry.grid(row=2, column=1, sticky=W, pady=3, padx=3)
		sec1name_Label.grid(row=3, column=0, sticky=E, pady=3, padx=3)
		sec1name_Entry.grid(row=3, column=1, sticky=W, pady=3, padx=3)
		sec2name_Label.grid(row=4, column=0, sticky=E, pady=3, padx=3)
		sec2name_Entry.grid(row=4, column=1, sticky=W, pady=3, padx=3)
		sec3name_Label.grid(row=5, column=0, sticky=E, pady=3, padx=3)
		sec3name_Entry.grid(row=5, column=1, sticky=W, pady=3, padx=3)
		DocLabel_2.grid(row=6, column=0, columnspan=2, pady=3, padx=3)
		DocLabel_3.grid(row=7, column=0, columnspan=2, pady=3, padx=3)
		DocLabel_4.grid(row=8, column=0, columnspan=2, pady=3, padx=3)
		
		okButton.grid(row=9, column=0, columnspan=2, pady=3, padx=3)
		DocLabel_5.grid(row=10, column=0, columnspan=2, pady=3, padx=3)
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
	
	def createSec(self, secname, bkuserid):
		Section = '''
    [{secname}]
    path = /mybk/{secname}
    auth users = {bkuserid}
    uid = root
    gid = root
    secrets file = /etc/rsyncd.secrets
    read only = no
'''
		Section = Section.format(**locals())
		self.rSyncdConf = self.rSyncdConf + Section
	
	def ok(self, event=None):
		isdataok = "T"
		rSyncdSecrets = ""
		bkuser_id = ""
		bkuser_pwd = ""
		sec1name = ""
		sec2name = ""
		sec3name = ""
		
		bkuser_id = self.bkuser_id_Var.get()
		bkuser_pwd = self.bkuser_pwd_Var.get()
		sec1name = self.sec1name_Var.get()
		sec2name = self.sec2name_Var.get()
		sec3name = self.sec3name_Var.get()
				
		bkuser_id = bkuser_id.strip()
		bkuser_pwd = bkuser_pwd.strip()
		sec1name = sec1name.strip()
		sec2name = sec2name.strip()
		sec3name = sec3name.strip()
		self.accpeted = True
		
		# data check 
		if bkuser_id == "":
			isdataok = "F"
			showerror(title="資訊不足", message="BKUser ID 沒填！")
		elif bkuser_pwd == "":
			isdataok = "F"
			showerror(title="資訊不足", message="BKUser 密碼沒填")
		elif sec1name == "":
			isdataok = "F"
			showerror(title="資訊不足", message="區段一名稱沒填")
		
		if isdataok == "T":
			self.createSec( sec1name, bkuser_id )
			if sec2name != "":
				self.createSec( sec2name, bkuser_id )
			if sec3name != "":
				self.createSec( sec3name, bkuser_id )
			rSyncdSecrets = bkuser_id + ":" + bkuser_pwd
			self.confw( "/etc/rsyncd.secrets", rSyncdSecrets )
			self.confw( "/etc/rsyncd.conf" , self.rSyncdConf )
			self.confw( "/etc/default/rsync", self.EtcDefaultRsync )
			subprocess.check_call(["/bin/chmod", "400", "/etc/rsyncd.secrets"])
			if not os.path.isdir( "/mybk" ):
				subprocess.check_call(["/bin/mkdir", "/mybk/"])
			if sec1name != "" and not os.path.isdir( "/mybk/"+sec1name ):
				subprocess.check_call(["/bin/mkdir", "/mybk/"+sec1name])
			if sec2name != "" and not os.path.isdir( "/mybk/"+sec2name ):
				subprocess.check_call(["/bin/mkdir", "/mybk/"+sec2name])
			if sec3name != "" and not os.path.isdir( "/mybk/"+sec3name ):
				subprocess.check_call(["/bin/mkdir", "/mybk/"+sec3name])
			showinfo( title="完工", message="rSync Server 設定完成，請重新啟動 rsync 伺服器！" )
		
	def close(self, event=None):
		self.master.destroy()
	

app = MainWindow()
scrX = app.master.winfo_screenwidth()
scrY = app.master.winfo_screenheight()
mX = int(scrX/2 - 210)
mY = int(scrY/2 - 155) - 80
strGeometry = "420x310+{0}+{1}".format(mX,mY)
app.master.geometry(strGeometry)
app.master.title("rSync Server 設定檔產生器")
app.master.protocol("WM_DELETE_WINDOW", app.quit)
showinfo(title="免責聲明", message="本程式依GPLv2授權, 僅方便您的使用, 並不提供任何執行成果的保證。" )
app.mainloop()

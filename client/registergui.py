#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import wx
import sys
class myregister(wx.Frame):
	def __init__(self,parent,prot=None):
		wx.Frame.__init__(self,None,title='register')
		self.SetSizeHintsSz((430,200),(430,200))
		self.protocol=prot
		self.app=parent
		panel=wx.Panel(self)
		username_label=wx.StaticText(panel,label='username')
		self.username=wx.TextCtrl(panel)
		password_label=wx.StaticText(panel,label='password')
		repassword_label=wx.StaticText(panel,label='repassword')
		self.password=wx.TextCtrl(panel,style=wx.TE_PASSWORD)
		self.repassword=wx.TextCtrl(panel,style=wx.TE_PASSWORD)
		self.status=wx.StaticText(panel,label='welcome to register')
		okbutton=wx.Button(panel,label='ok')
		okbutton.Bind(wx.EVT_BUTTON,self.okaction)
		exitbutton=wx.Button(panel,label='exit')
		exitbutton.Bind(wx.EVT_BUTTON,self.exitaction)
		hbox1=wx.BoxSizer()
		hbox1.Add(username_label,proportion=1,flag=wx.LEFT,border=5)
		hbox1.Add(self.username,proportion=4,flag=wx.EXPAND|wx.ALL,border=5)
		hbox2=wx.BoxSizer()
		hbox2.Add(password_label,proportion=1,flag=wx.LEFT,border=5)
		hbox2.Add(self.password,proportion=4,flag=wx.EXPAND|wx.ALL,border=5)
		hbox3=wx.BoxSizer()
		hbox3.Add(repassword_label,proportion=1,flag=wx.LEFT,border=5)
		hbox3.Add(self.repassword,proportion=3,flag=wx.EXPAND|wx.ALL,border=5)
		hbox4=wx.BoxSizer()
		hbox4.Add(okbutton,proportion=1,flag=wx.LEFT,border=10)
		hbox4.Add(exitbutton,proportion=1,flag=wx.RIGHT,border=10)
		vbox1=wx.BoxSizer(wx.VERTICAL)
		vbox1.Add(hbox1,proportion=1,border=5)
		vbox1.Add(hbox2,proportion=1,border=5)
		vbox1.Add(hbox3,proportion=1,border=5)
		vbox1.Add(hbox4,proportion=1,border=5)
		vbox1.Add(self.status,proportion=1,border=5)
		panel.SetSizer(vbox1)
	def setprotocol(self,prot):
		self.protocol=prot
	def okaction(self,evt):
		password=self.password.GetValue().strip()
		repassword=self.repassword.GetValue().strip()
		username=self.username.GetValue()
		if username !='' and password!='' and repassword !='':
			if password!=repassword:
				self.status.SetLabel('password must be same with repassword')
			else:
				content='Register:{0}--{1}'.format(username,password)
				self.protocol.sendLine(content)


		
		else:
			self.status.SetLabel('must fill the information')
	def exitaction(self,evt):
		self.status.SetLabel('exit')
	def registerdestroy(self):
		self.Destroy()
#if __name__=='__main__':
#	app=wx.App()
#	myf=myregister(None,None)
#	myf.Show()
#	app.MainLoop()
	

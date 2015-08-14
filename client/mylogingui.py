#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import wx
import registergui
class mylogingui(object):
	def __init__(self,app,proc=None):
		self.protocol=proc
		self.app=app
		self.frame=wx.Frame(None,title='login',size=(400,200))
		self.frame.SetMinSize((400,200))
		self.frame.SetMaxSize((400,200))
		self.bkg=wx.Panel(self.frame)
		self.loginbutton=wx.Button(self.bkg,label='login')
		self.loginbutton.Bind(wx.EVT_BUTTON,self.loginaction)
		self.registerbutton=wx.Button(self.bkg,label='register')
		self.registerbutton.Bind(wx.EVT_BUTTON,self.registeraction)
		self.username=wx.TextCtrl(self.bkg)
		self.password=wx.TextCtrl(self.bkg,style=wx.TE_PASSWORD)
		self.username_label=wx.StaticText(self.bkg,label='username')
		self.password_label=wx.StaticText(self.bkg,label='password')
		self.hbox1=wx.BoxSizer()
		self.hbox1.Add(self.username_label,proportion=1)
		self.hbox1.Add(self.username,proportion=4,flag=wx.ALL|wx.RIGHT,border=5)
		self.hbox2=wx.BoxSizer()
		self.hbox2.Add(self.password_label,proportion=1)
		self.hbox2.Add(self.password,proportion=4,flag=wx.ALL|wx.RIGHT,border=5)
		self.hbox3=wx.BoxSizer()
		self.hbox3.Add(self.loginbutton,proportion=2,flag=wx.ALIGN_CENTER)
		self.hbox3.Add(self.registerbutton,proportion=2,flag=wx.ALIGN_CENTER)
		self.hbox4=wx.BoxSizer()
		self.status=wx.StaticText(self.bkg,label='status')
		self.hbox4.Add(self.status,proportion=1,flag=wx.ALIGN_CENTER|wx.ALL)
		self.vbox=wx.BoxSizer(wx.VERTICAL)
		self.vbox.Add(self.hbox1,proportion=0,border=5)
		self.vbox.Add(self.hbox2,proportion=0,border=5)
		self.vbox.Add(self.hbox3,proportion=0,border=5)
		self.vbox.Add(self.hbox4,proportion=0,border=5)
		self.bkg.SetSizer(self.vbox)
		
	def setprotocol(self,prot):
		self.protocol=prot
	def loginaction(self,evt):
		username=self.username.GetValue().strip()
		password=self.password.GetValue().strip()
		cmd='{0} {1}'.format(username,password)
		self.protocol.sendLine(cmd)
	def senddata(self,cmd):
		self.protocol.sendLine(cmd)
	def registeraction(self,evt):
		register=registergui.myregister(self.app,self.protocol)
		self.logindestroy()
		register.Show()
	def loginshow(self):
		self.frame.Show()
	def logindestroy(self):
		self.frame.Destroy()
		
if __name__=='__main__':
	mygui=mylogingui(None)
	mygui.loginshow()
		

#!/usr/bin/python
#!_*_ coding:utf-8 _*_
#from twisted.internet import wxreactor
#wxreactor.install()
from twisted.internet import reactor,protocol
from twisted.protocols.basic import LineReceiver
import wx
import threading
import time
class chatgui(object):
	def __init__(self,app,prot,name):
		self.protocol=prot
		self.app=app
		self.name=name
		self.frame=wx.Frame(None,title='chat:%s'%self.name,size=(400,400))
		self.frame.SetMinSize((400,400))
		self.frame.SetMaxSize((400,400))
		self.frame.Bind(wx.EVT_CLOSE,self.testclose)
		self.bkg=wx.Panel(self.frame)
		self.chatcontent=wx.TextCtrl(self.bkg,style=wx.TE_MULTILINE | wx.VSCROLL |wx.HSCROLL)
		self.inputcontent=wx.TextCtrl(self.bkg,style=wx.TE_MULTILINE |wx.HSCROLL)
		self.userlist=wx.ListBox(self.bkg,26,wx.DefaultPosition,(150,400),['All Users'],wx.LB_SINGLE)
		self.userlist.SetSelection(0)
		self.userlist.Bind(wx.EVT_LISTBOX, self.OnSelect)
		self.sendbutton=wx.Button(self.bkg,label='send')
		self.sendbutton.Bind(wx.EVT_BUTTON,self.sendmessage)
		self.touser=wx.StaticText(self.bkg,label='To All Users:')
		self.hbox1=wx.BoxSizer()
		self.hbox1.Add(self.inputcontent,proportion=2,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox1.Add(self.sendbutton,proportion=1,flag=wx.LEFT|wx.ALIGN_CENTER,border=0)
		self.vbox1=wx.BoxSizer(wx.VERTICAL)
		self.vbox1.Add(self.chatcontent,proportion=1,flag=wx.ALL|wx.EXPAND,border=5)
		self.vbox1.Add(self.touser,proportion=0,flag=wx.ALL|wx.LEFT|wx.RIGHT,border=5)
		self.vbox1.Add(self.hbox1,proportion=0,flag=wx.BOTTOM|wx.LEFT|wx.RIGHT,border=5)
		self.hbox2=wx.BoxSizer()
		self.hbox2.Add(self.vbox1,proportion=2,flag=wx.EXPAND|wx.ALL,border=5)
		self.hbox2.Add(self.userlist,proportion=1,flag=wx.RIGHT,border=10)
		self.bkg.SetSizer(self.hbox2)
		self.mythr=mythread(self.protocol,self.userlist)
		self.mythr.setDaemon(1)
		self.mythr.start()
	def testclose(self,evt):
		self.app.Exit()
	def OnSelect(self,evt):
		index=evt.GetSelection()
		value=self.userlist.GetString(index)
		self.touser.SetLabel('To %s:'%value)
	
	def chatshow(self):
		self.frame.Show()
	def sendmessage(self,evt):
		content=str(self.inputcontent.GetValue())
		to=str(self.touser.GetLabel())	
		to=to[to.find(' ')+1:len(to)-1]
		if self.name!=to:
			self.protocol.sendLine("{0}:{1}".format(to,content))
		else:
#			wx.MessageBox('can not chat with yourself',caption='Message',style=wx.OK)
			dlg=wx.MessageDialog(self.bkg,'Can not chat with yourself',caption='Message',style=wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
class mythread(threading.Thread):
	def __init__(self,proc,userlist):
		threading.Thread.__init__(self)
		self.status=True
		self.proc=proc
		self.userlist=userlist
	def run(self):	
		while self.status:
			userl='--'.join(self.userlist.GetStrings())
			self.proc.sendLine('UserList:{0}'.format(userl))
			time.sleep(2)
	def setstatus(self,s):
		self.status=s
		
#if __name__=='__main__':
#	app=wx.App(False)
#	chat=chatgui(app,None,None)
#	chat.chatshow()
#	reactor.registerWxApp(app)
#	reactor.connectTCP('127.0.0.1',12345,myfactory(chat))
#	reactor.run()
	

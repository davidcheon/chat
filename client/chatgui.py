#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor,protocol
from twisted.protocols.basic import LineReceiver
import wx
import threading

class chatgui(object):
	def __init__(self,app,prot):
		self.protocol=prot
		self.app=app
		self.frame=wx.Frame(None,title='chat',size=(400,400))
		self.frame.SetMinSize((400,400))
		self.frame.SetMaxSize((400,400))
		self.bkg=wx.Panel(self.frame)
		self.chatcontent=wx.TextCtrl(self.bkg,style=wx.TE_MULTILINE | wx.VSCROLL |wx.HSCROLL)
		self.inputcontent=wx.TextCtrl(self.bkg,style=wx.TE_MULTILINE |wx.HSCROLL)
		self.userlist=wx.ListBox(self.bkg,26,wx.DefaultPosition,(150,400),['All Users','a','b','c','d','e','f','g','h','i'],wx.LB_SINGLE)
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
	def OnSelect(self,evt):
		index=evt.GetSelection()
		value=self.userlist.GetString(index)
		self.touser.SetLabel('To %s:'%value)
	def chatshow(self):
		self.frame.Show()
	def sendmessage(self,evt):
		pass
		
class myprotocol(LineReceiver):
	def __init__(self,gui):
		self.gui=gui
		self.content=self.gui.chatcontent
	def connectionLost(self,reason):
		print 'lost:'+reason.getErrorMessage()
		reactor.stop()
	def lineReceived(self,line):
		self.content.AppendText(line+'\n')

class myfactory(protocol.ClientFactory):
	def __init__(self,gui):
		self.gui=gui
	def buildProtocol(self,addr):
		return myprotocol(self.gui)
		
if __name__=='__main__':
	app=wx.App(False)
	chat=chatgui(app,None)
	chat.chatshow()
	reactor.registerWxApp(app)
	reactor.connectTCP('127.0.0.1',12345,myfactory(chat))
	reactor.run()
	

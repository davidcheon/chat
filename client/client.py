#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.internet import wxreactor
wxreactor.install()
import mylogingui,chatgui
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver
import threading
import time
import wx
class myprotocol(LineReceiver):
	def __init__(self):
		self.gui=None
		self.status=None
	def connectionLost(self,reason):
		print 'lost:'+reason.getErrorMessage()
	def lineReceived(self,line):
		self.gui.setprotocol(self)
		if self.status!='start chat':
			if line.split(':')[0]=='login succeed':
				self.chat=chatgui.chatgui(self.gui.app,self,line.split(':')[1])
				self.chat.chatshow()
				self.gui.logindestroy()
				self.status='start chat'
			else:
				self.gui.status.SetLabel(line)
		else:
			self.chat.chatcontent.AppendText(line+'\n')
		
	def connectionMade(self):
		self.gui=self.factory.gui
class myfactory(protocol.ClientFactory):
	def __init__(self,gui):
		self.gui=gui
		self.protocol=myprotocol
#	def buildProtocol(self,addr):
#		return myprotocol()
	def clientConnectionFailed(self,transport,reason):
		reactor.stop()
	def clientConnectionLost(self,transport,reason):
		reactor.stop
if __name__=='__main__':
	app=wx.App(False)
	
	mygui=mylogingui.mylogingui(app)
	myfac=myfactory(mygui)
	
	reactor.registerWxApp(app)
	
	mygui.loginshow()
	
	reactor.connectTCP('192.168.0.15',12345,myfac)
	
	reactor.run()
	
	



#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import mylogingui,chatgui
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver
import threading
import time
import wx
class myprotocol(LineReceiver):
	def __init__(self):
		self.gui=mylogingui.mylogingui(self)
		self.gui.loginshow()
	def connectionLost(self,reason):
		print 'lost:'+reason.getErrorMessage()
	def lineReceived(self,line):
		self.gui.status.SetLabel(line)
		print line
		if line=='login succeed':
			self.gui.logindestroy()
			chat=chatgui.chatgui(self.gui.app,self)
			chat.chatshow()
	def connectionMade(self):
		print 'connection made'
class myfactory(protocol.ClientFactory):
	
	def buildProtocol(self,addr):
		return myprotocol()
		
if __name__=='__main__':
	app=wx.App(False)
	reactor.registerWxApp(app)
	reactor.connectTCP('192.168.0.47',12345,myfactory())
	reactor.run()
	



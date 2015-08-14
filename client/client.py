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
from ConfigParser import ConfigParser
import commands
import myregister
class myprotocol(LineReceiver):
	def __init__(self):
		self.gui=None
		self.status=None
	def connectionLost(self,reason):
		print 'connection lost:'+reason.getErrorMessage()
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
			if not line.startswith('UserList:'):
				self.chat.chatcontent.AppendText(line+'\n')
			else:
				line=line[len('UserList:'):]
				users=line.split(':')
				#print users
				#self.chat.userlist.Clear()
				#self.chat.userlist.Append('All Users')
				
				for u in users:
					self.chat.userlist.Append(u)	
	def connectionMade(self):
		self.gui=self.factory.gui
		self.reg=self.factory.reg
class myfactory(protocol.ClientFactory):
	def __init__(self,gui,reg):
		self.gui=gui
		self.reg=reg
		self.protocol=myprotocol
#	def buildProtocol(self,addr):
#		return myprotocol()
	def clientConnectionFailed(self,transport,reason):
		reactor.stop()
	def clientConnectionLost(self,transport,reason):
		reactor.stop
def getipaddress():
	return commands.getoutput("ifconfig wlan0|grep -i 'inet '|awk '{print $2}'|awk -F':' '{print $2}'")
if __name__=='__main__':
	CONFIGFILE='../config.txt'
	config=ConfigParser()
	config.read(CONFIGFILE)
	ip=config.get('options','ip') if config.get('options','ip')!='' else getipaddress()
	port=config.getint('options','port')
	app=wx.App(False)
	
	mygui=mylogingui.mylogingui(app)
	myreg=myregister.myregister(app)
	myfac=myfactory(mygui,myreg)
	
	reactor.registerWxApp(app)
	
	mygui.loginshow()
	
	reactor.connectTCP(ip,port,myfac)
	
	reactor.run()
	
	



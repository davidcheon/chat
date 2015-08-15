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
import registergui
class myprotocol(LineReceiver):
	def __init__(self):
		self.gui=None
		self.reg=None
		self.status=None
	def connectionLost(self,reason):
		print 'connection lost:'+reason.getErrorMessage()
	def lineReceived(self,line):
		#self.gui.setprotocol(self)
		#self.reg.setprotocol(self)
		if self.status!='start chat':
			if line.startswith('login succeed'):
				self.chat=chatgui.chatgui(self.gui.app,self,line.split(':')[1])
				self.chat.chatshow()
				self.gui.logindestroy()
				self.status='start chat'
			elif line.startswith('Register succeed'):
				self.chat=chatgui.chatgui(self.reg.app,self,line.split(':')[1])
				self.chat.chatshow()
				self.reg.registerdestroy()
				self.status='start chat'
			else:
				if line.startswith('Register Error:'):
					self.reg.status.SetLabel(line)
				else:
					self.gui.status.SetLabel(line)
		else:
			if line.startswith('RemoveUserList:'):
				users=self.chat.userlist.GetStrings()
				line=line[len('RemoveUserList:'):]
				serverusers=line.split(':')				
				for u in serverusers:
					self.chat.userlist.Delete(self.chat.userlist.FindString(u))
			elif line.startswith('AddUserList:'):
				line=line[len('AddUserList:'):]
				users=line.split(':')
				for u in users:
					self.chat.userlist.Append(u)	
			else:
				self.chat.chatcontent.AppendText(line+'\n')
	def connectionMade(self):
		self.gui=self.factory.gui
		self.reg=self.gui.register
		self.gui.setprotocol(self)
		self.reg.setprotocol(self)
class myfactory(protocol.ClientFactory):
	def __init__(self,gui):
		self.gui=gui
		self.protocol=myprotocol
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
	myfac=myfactory(mygui)
	
	reactor.registerWxApp(app)
	
	mygui.loginshow()
	
	reactor.connectTCP(ip,port,myfac)
	
	reactor.run()
	
	



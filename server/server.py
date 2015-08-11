#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.intenet import protocol,reactor
from twisted.protocol.basic import LineReceiver
class myprotocol(protocol.Protocol):
	def __init__(self,users):
		self.users=users
		self.name=None
		self.status='GET Name'
	def connectionMade(self):
		pass
	def lineReceived(self,line):
		pass
	def connectionLost(self,reason):
		pass
class myfactory(protocol.Factory):
	def __init__(self):
	self.users={}
	def buildProtocol(self):
		return myprotocol(self.users)
myf=myfactory()
reactor.ListenTCP(12345,myf)
reactor.run()

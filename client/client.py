#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.internet import protocol,reactor
from twisted.protocol.basic import LineReceiver
class myprotocol(protocol.Protocol):
	def connectionMade(self):
		pass
	def connectionLost(self,reason):
		pass
	def lineReceived(self,line):
		pass
class myfactory(protocol.Factory):
	def buildProtocol(self):
		return myprotocol()


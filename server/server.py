#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver
import hashlib
import sqlite3
class myprotocol(LineReceiver):
	def __init__(self,users):
		self.users=users
		self.name=None
		self.status='GET Name'
		self.conn=sqlite3.connect('my.db')
		self.curs=self.conn.cursor()
		self.md5=hashlib.md5()
	def connectionMade(self):
		self.sendLine('welcome to chat system')
	def lineReceived(self,line):
		if self.status =='GET Name':
			if self.handle_login(line):
				self.status='Login Succeed'
		elif self.status=='Login Succeed':
			self.handle_others(line)
	def handle_others(self,cmd):
		name,content=self.splitcmd(cmd)
		print 'name:',name,'cont:',content
		content='%s To %s said:%s\n'%(self.name,name,content)
		if name=='All Users':
			for n,l in self.users.items():
				if n!=name:
					
					l.sendLine(content)
		else:
			for n,l in self.users.items():
				if n==name:
					l.sendLine(content)
					break
				
	def splitcmd(self,cmd):
		return cmd.split(':')


	def handle_login(self,line):
		name,passwd=self.splitinput(line)
		query='select * from users where username = "%s"'%name
		self.curs.execute(query)
		result=self.curs.fetchall()
		if len(result)<1:
			self.sendLine('no have username:%s'%name)
			return False
		else:
			self.md5.update(passwd.strip())
			passwd=self.md5.hexdigest()
			query='select * from users where username = "%s" and password = "%s"' %(name,passwd)
			self.curs.execute(query)
			result=self.curs.fetchall()
			if len(result)<1:
				self.sendLine('wrong username or password')
				return False
		self.name=name
		self.users[name]=self
		self.sendLine('login succeed:{0}'.format(self.name))
		return True
	def splitinput(self,line):
		name,passwd=line.strip().split()
		return name.strip(),passwd.strip()
	def connectionLost(self,reason):
		self.curs.close()
		self.conn.close()
		print 'connection lost:'+reason.getErrorMessage()
class myfactory(protocol.Factory):
	def __init__(self):
		self.users={}
	def buildProtocol(self,addr):
		return myprotocol(self.users)
if __name__=='__main__':
	myf=myfactory()
	reactor.listenTCP(12345,myf)
	reactor.run()

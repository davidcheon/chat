#!/usr/bin/python
#!_*_ coding:utf-8 _*_
from twisted.internet import protocol,reactor
from twisted.protocols.basic import LineReceiver
import hashlib
import sqlite3
from ConfigParser import ConfigParser
class myprotocol(LineReceiver):
	def __init__(self,users):
		self.users=users
		self.name=None
		self.status='GET Name'
		
		self.conn=sqlite3.connect('my.db')
		self.curs=self.conn.cursor()
	def connectionMade(self):
		self.sendLine('welcome to chat system')
	def lineReceived(self,line):
		if self.status =='GET Name':
			if line.startswith('Register:'):
				if self.handle_register(line):
					self.status='Register Succeed'
			else:
				if self.handle_login(line):
					self.status='Login Succeed'
		elif self.status=='Login Succeed':
			self.handle_others(line)
		elif self.status=='Register Succeed':
			self.handle_others(line)
	def handle_register(self,line):
		action,contentorig=self.splitcmd(line)
		name,password=contentorig.split('--')
		search='select * from users where username="%s"'%name
		resu=self.curs.execute(search).fetchall()
		if resu==[]:
			self.md5=hashlib.md5()
			self.md5.update(password)
			cmd='insert into users(username,password) values("%s","%s")'%(name,self.md5.hexdigest())
			self.curs.execute(cmd)
			self.conn.commit()
			
			self.name=name
			self.users[name]=self
			self.sendLine('Register succeed:{0}'.format(name))
			return True
		else:
			self.sendLine('Register Error:%s already registered,try another name'%name)
			return False
			
	def handle_others(self,cmd):
		name,contentorig=self.splitcmd(cmd)
		content='%s To %s said:%s\n'%(self.name,name,contentorig)
		if name=='All Users':
			for n,l in self.users.items():
				if  n!='All Users':
					
					l.sendLine(content)
		elif name=='UserList':
			ld=None
			clientusers=set(contentorig.split('--'))
			serverusers=set(self.users.keys())
			ls=list(serverusers-clientusers)
			if ls!=[]:
				for n,l in self.users.items():
					if n==self.name:
						ld=l
						break
				ul=':'.join(ls)
				ld.sendLine('AddUserList:%s'%ul)
			else:
				ls=list(clientusers-serverusers)
				if ls!=[]:
					for n,l in self.users.items():
						if n==self.name:
							ld=l
							break
					ul=':'.join(ls)
					ld.sendLine('RemoveUserList:%s'%ul)
		
		else:
			for n,l in self.users.items():
				if n==self.name:
					l.sendLine(content)
				if n==name:
					l.sendLine(content)
				
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
			self.md5=hashlib.md5()
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
		if self.users.has_key(self.name):
			self.users.pop(self.name)
		print 'connection lost:'+reason.getErrorMessage()
class myfactory(protocol.Factory):
	def __init__(self):
		self.users={'All Users':None}
	def buildProtocol(self,addr):
		return myprotocol(self.users)
if __name__=='__main__':
	CONFIGFILE='../config.txt'
	config=ConfigParser()
	config.read(CONFIGFILE)
	port=config.getint('options','port')
	myf=myfactory()
	reactor.listenTCP(port,myf)
	reactor.run()

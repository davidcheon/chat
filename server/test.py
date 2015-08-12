#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import sqlite3
import hashlib
conn=sqlite3.connect('my.db')
cursor=conn.cursor()
name='daisongchen'
md5=hashlib.md5()
md5.update('daisongchen')
pwd=md5.hexdigest()
cmd='insert into users(id,username,password) values ("%s","%s","%s")'%(2,name,pwd)
cursor.execute(cmd)
conn.commit()
cursor.close()
conn.close()

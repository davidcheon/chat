#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import sqlite3
conn=sqlite3.connect('../server/my.db')
cursor=conn.cursor()
cmd='select * from users'
cursor.execute(cmd)
print cursor.fetchall()
cursor.execute(cmd)
print cursor.fetchall()
cursor.execute(cmd)
print cursor.fetchall()
cursor.execute(cmd)
print cursor.fetchall()

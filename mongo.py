#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import string
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

conn = pymongo.MongoClient()
db = conn.putaoDB
usr = db.usr

usr.remove()

f = open("fortest.txt")
while True:
	usrID = f.readline()
	if usrID == "":
		break
	torID = f.readline()
	name = f.readline()
	print name
	ID = re.sub("\n", "", usrID)
	torID = re.sub("\n", "", torID)
	name = re.sub("\n", "", name)
	tor_doc = {"Title" : name, "torID" : torID}
	if usr.find_one({"ID" : ID}) != None:
		tmp_doc = usr.find_one({"ID" : ID})
		check = False
		for j in range(len(tmp_doc["Torrent"])):
			tmp = tmp_doc["Torrent"][j]
			if name == tmp["Title"]:
				check = True
				break
		if check == False:
			usr.update({"ID" : ID}, {"$push":{"Torrent" :tor_doc}})
		else:
			continue
	else:
		usr_doc = {"ID" : ID, "Torrent" : [tor_doc]}
		usr.insert(usr_doc)

while True:
	name = f.readline()
	if name == "":
		print "Finished!"
		break
	print name
	name = re.sub("\n", "", name)
	torID = f.readline()
	torID = re.sub("\n", "", torID)
	types = f.readline()
	types = re.sub("类别:","",types)
	types = re.sub("\n", "", types)
	watch = f.readline()
	watch = re.sub("查看量:","",watch)
	watch = re.sub("\n", "", watch)
	click = f.readline()
	click = re.sub("点击量:", "", click)
	click = re.sub("\n", "", click)
	finish = f.readline()
	finish = re.sub("完成量:", "", finish)
	finish = re.sub("\n", "", finish)
	tor_doc = {"Title" : name, "torID" : torID, "Type" : types, "查看量" : watch, "点击量" : click, "完成量" : finish}
	f.readline()
	
	while True:
		ID = f.readline()
		if "---END---" in ID:
			break
		ID = re.sub("\n", "", ID)
		sex = f.readline()
		sex = re.sub("\n", "", sex)
		kind = f.readline()
		kind = re.sub("\n", "", kind)
		if usr.find_one({"ID" : ID}) != None:
			tmp_doc = usr.find_one({"ID" : ID})
			check = False
			for j in range(len(tmp_doc["Torrent"])):
				tmp = tmp_doc["Torrent"][j]
				if name == tmp["Title"]:
					check = True
					break
			if check == False:
				usr.update({"ID" : ID}, {"$push":{"Torrent" :tor_doc}})
			else:
				continue
		else:
			usr_doc = {"ID" : ID, "sex" : sex, "kind" : kind, "Torrent" : [tor_doc]}
			usr.insert(usr_doc)

f.close()

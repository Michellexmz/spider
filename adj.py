# -*- coding: utf-8 -*-
import string
import re

ff = open("re.txt")
f = file("torrent.txt", 'w')
w = file("fortest.txt", "w")

while True:
	name = ff.readline()
	flag = False
	if name == "":
		break
	torID = ""
	torID = ff.readline()
	kind = ""
	if "类别" not in torID:
		kind = ff.readline()
	if "类别" not in kind:
		print name
		flag = True
	else:
		f.write(name+torID+kind)
	while True:
		line = ff.readline()
		if flag == False:
			f.write(line)
		if "第12个月" in line:
			break

while True:
	name = ff.readline()
	flag = False
	if name == "":
		break
	torID = ff.readline()
	kind = ff.readline()
	watch = ff.readline()
	click = ff.readline()
	finish = ff.readline()
	f.write(name + torID + kind + watch + click + finish)
	line = ff.readline()
	f.write(line)
	while  True:
		usrID = ff.readline()
		if "平均分享率" in usrID:
			break
		lifespan = ff.readline()
		share = ff.readline()
		if "生" in share:
			sex = share
		else:
			sex = ff.readline()
		kind = ff.readline()
		f.write(usrID + sex + kind)
	while True:
		line = ff.readline()
		if "第12个月" in line:
			f.write("---END---\n")
			break

while True:
	name = ff.readline()
	flag = False
	if name == "":
		break
	torID = ff.readline()
	kind = ff.readline()
	watch = ff.readline()
	click = ff.readline()
	finish = ff.readline()
	line = ff.readline()
	count = 0
	while True:
		usrID = ff.readline()
		usrID = re.sub("\n", "", usrID)
		if "平均分享率" in usrID:
			break
		lifespan = ff.readline()
		share = ff.readline()
		if "生" in share:
			flag = True
			print name, usrID, count
			break
		sex = ff.readline()
		kind = ff.readline()
		count = count + 1
	if flag == True:
		break
	while  True:
		line = ff.readline()
		if "第12个月" in line:
			break

line = ff.readline()
while True:
	if "title" in line:
		ff.readline()
		line = ff.readline()
		if "torrent ID" in line:
			ID = ff.readline()
			line = ff.readline()
			if "user ID" in line:
				line =ff.readline()
				line = re.sub("\n","",line)
				while line.isdigit():
					line = ff.readline()
					line = re.sub("\n","",line)
				if "title" in line:
					continue
				else:
					print ID
	elif line == "":
		break

line = ff.readline()
while True:
	if line == "":
		print "finished"
		break
	name = ff.readline()
	print name
	f.write(name)
	ff.readline()
	torID = ff.readline()
	f.write(torID)
	f.write("\n")
	line = ff.readline()
	while "title" not in line:
		if line == "":
			break
		line = ff.readline()
		usrID = line
		#usrID = re.sub("\n","",line)
		w.write( usrID + torID + name)
	if "title" in line:
		continue
	else:
		break

w.close()
f.close()
ff.close()
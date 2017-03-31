#!/usr/bin/env python
# -*- coding: utf-8 -*-
import StringIO
import gzip
import urllib
import urllib2
import httplib
from bs4 import BeautifulSoup
import re
import string
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

home_url = 'https://pt.sjtu.edu.cn/'
torrents_list_url = 'https://pt.sjtu.edu.cn/torrents.php'

def getPage(url):
    request = urllib2.Request(url)
    request.add_header("cookie","PHPSESSID=e437f03cc758ee4171d1212c3d33b9b9; bgPicName=Default; __utmt=1; c_expiresintv=0; c_secure_uid=ODIyNTE%3D; c_secure_pass=eff4b6141c0066a96e2b2eeebcc8485a; c_secure_ssl=eWVhaA%3D%3D; c_secure_login=bm9wZQ%3D%3D; __utma=248584774.1646623820.1458039768.1458039768.1458044708.2; __utmb=248584774.3.10.1458044708; __utmc=248584774; __utmz=248584774.1458039768.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)")
    request.add_header("user-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36")
    request.add_header("accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    request.add_header("accept-encoding","gzip, deflate, sdch")
    request.add_header("referer","https://pt.sjtu.edu.cn/index.php")
    response = urllib2.urlopen(request, timeout = 10)
    content = StringIO.StringIO(response.read())
    html = gzip.GzipFile(fileobj = content)
    return html.read()

TRIES = 5
def main():
    list_head_doc = getPage(torrents_list_url)
    soup = BeautifulSoup(list_head_doc)
    page_outer = soup.html.body.findAll(attrs = {"class" : "outer"})
    
    list_url_base = "https://pt.sjtu.edu.cn/torrents.php?inclbookmarked=0&incldead=0&spstate=0&page="
    torrent_file = file('spider.txt', 'w')

    class Torrent:
        def _init_(self):
            self.torrent_title = ''
            self.type = ''

    torrent = Torrent()

    for i in range(50):
        print "Crawing  Page " + str(i)
        list_url = list_url_base + str(i)              
        for retry in range(TRIES):
            list_doc = getPage(list_url)
            if list_doc != 'MyError':
                break
        if list_doc == 'MyError':                   #访问超时
            print "##Time Out## User List Page: " + str(i)
            continue

        soup = BeautifulSoup(list_url)

        page_outer = soup.html.body.findAll(attrs = {"class" : "outer"})
        soup = BeautifulSoup(str(page_outer))

        torrent_types = soup.findAll(attrs = {"class" : "nobr"})
        keyword_a = re.compile("pic\/category\/chd\/colytorrents\/chs\/.*\.png")
        torrenttype_doc = soup.findAll(attrs = {"src" : keyword_a})

        keyword_b = re.compile("details\.php.*id=.*\&hit=\d\&hitfrom=.*")
        torrent_name = soup.findAll(attrs = {"href" : keyword_b})

        for j in range(len(torrent_name)):
            torrent_type = torrenttype_doc[j+27]['alt']
            torrent_title = torrent_name[j].b.text
            print torrent_title + " "
            torrent_file.write(torrent_type + ' ' + torrent_title +'\n')

    torrent_file.close()

if __name__ == '__main__':
    main()
    print "Spider Complete!"
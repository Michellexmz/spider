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
import os

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

    class Torrent:
        def _init_(self):
            self.torrent_title = ''
            self.type = ''

    torrent = Torrent()

    for i in range(4):
        print "Crawing  Page " + str(i)
        list_url = list_url_base + str(i)
        list_doc = ""              
        for retry in range(TRIES):
            list_doc = getPage(list_url)
            if list_doc != 'MyError':
                break
        if list_doc == 'Error':                   #访问超时
            print "##Time Out## User List Page: " + str(i)
            continue

        soup = BeautifulSoup(list_doc)

        page_outer = soup.html.body.findAll(attrs = {"class" : "outer"})
        soup = BeautifulSoup(str(page_outer))

        keyword = re.compile("details\.php.*id=.*\&hit=\d\&hitfrom=.*")
        torrents_id = soup.findAll(attrs={"href" : keyword})
        for j in range(len(torrents_id)):

            num = i * 50 + j + 1
            print "Crawing Torrent " + str(num)
            
            torrent = Torrent()
            page_outer = soup.html.body.findAll(attrs = {"class" : "outer"})
            soup = BeautifulSoup(str(page_outer))

            torrent_types = soup.findAll(attrs = {"class" : "nobr"})
            keyword_a = re.compile("pic\/category\/chd\/colytorrents\/chs\/.*\.png")
            torrenttype_doc = soup.findAll(attrs = {"src" : keyword_a})

            torrent_type = torrenttype_doc[j+27]['alt']                     
            typelist = ['华语电影', '欧美电影', '亚洲电影', '纪录片', '港台电视剧', '亚洲电视剧'\
            '大陆电视剧', '欧美电视剧', '大陆综艺节目', '港台综艺节目', '欧美综艺节目', '日韩综艺节目']
            check = False
            for m in range(len(typelist)):
                if typelist[m]==torrent_type:
                    check = True

            if check == False:
                continue

            torrents_id[j] = torrents_id[j]['href']
            torrent.uid = re.sub(".*id=(\d+)\&hit.*", "\g<1>", torrents_id[j])
            torrentid_url = home_url + 'details.php?id=' + torrent.uid
            dirts_name = 'torrent' + str(num)
            os.makedirs(dirts_name)

            file_name = dirts_name + '/maincode.txt'
            torrent_file = file(file_name , 'w')
            torrentid_doc = getPage(torrentid_url)
            print "Copying torrent " + str(num) + " Main Source Code..."
            torrent_file.writelines(torrentid_doc)
            torrent_file.close()

            hotlist = re.compile(r'<tr>.+?热度表.+?</tr>')
            matches = hotlist.findall(torrentid_doc)
            for match in matches:
                time_id =  re.sub("<tr.*<a href=.*id=(\d.+)'><b>.*", "\g<1>", match)
                time_head_url = home_url + 'viewsnatches.php?id=' + time_id
                time_head_doc = getPage(time_head_url)
                soup = BeautifulSoup(time_head_doc)
                
                keyword = re.compile("viewsnatches.*completedat.*page=.*")
                page_nums = soup.findAll(attrs = {"href" : keyword})
                page_nums.pop()
                last_list = (page_nums.pop())['href']
                lists_nums = int(re.sub(".*=", '', last_list))
                
                for k in range(lists_nums):
                    time_url = home_url + 'viewsnatches.php?id=' + time_id + '&sort=completedat&page=' + str(k)
                    time_doc = getPage(time_url)
                    timefile_name = dirts_name + '/timecode' + str(k) + '.txt'
                    torrent_file = file(timefile_name, 'w')
                    print "Copying Time Code Page " + str(k) + "..."
                    torrent_file.writelines(time_doc)
                    torrent_file.close()

                    time.sleep(5)

            time.sleep(5)


if __name__ == '__main__':
    main()
    print "Spider Complete!"
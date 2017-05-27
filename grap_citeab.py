#!/usr/bin/env python3
# -* conding: utf-8 *-
'The program of graping citeab.com'

__author__ = 'liudongdong'

#from urllib import request #引入urlib模块
import urllib
import beautifulscraper
import re
import MySQLdb
values = {"username":"1096093035@qq.com","password":"XXXX"}
urllib.request.ProxyHandler({'https':'127.0.0.1'})
responses = urllib.request.Request("https://www.citeab.com/browse/suppliers",None,{'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)','Referer':'https://www.citeab.com'})
try:
  result = urllib.request.urlopen(responses)
  
except urllib.error.HTTPError as e:
   print(e.code)
except urllib.error.URLError as e:
   print(e.reason)
content = result.read().decode("utf-8")
#urllib.request.urlretrieve("https://www.citeab.com/browse/suppliers","D:\pythonprojects\citeab.html")
print(content)
pattern = re.compile('<li>.*?<h6>.*?<a.*?"/browse/suppliers/(.*?)">.*?"/browse/suppliers/(.*?)".*?</a>.*?</h6>.*?</li>',re.S)
#pattern = re.compile('<li>.*?<h6>.*?<a.*?">"(.*?)"</a>.*?</h6>.*?</li>',re.S)
#pattern = re.compile(r'2012-2017',re.S)
items = re.findall(pattern,content)
#print(len(items))
#print(items)
db = MySQLdb._mysql.connect("localhost","root","","citeab")

for item in items:
  print(item[0],item[1])
  sql = "insert into suppliers(name,website) values('%s','%s')" % (item[0],'https://www.citeab.com/browse/suppliers/'+item[0])

  sql1 = "insert into suppliers(name,website) values('%s','%s')" % (item[1],'https://www.citeab.com/browse/suppliers/'+item[1])
  #数据存储
  db.query(sql)
  db.query(sql1)

  









  
#print(urllib.request.getcode())
#urllib.request.urlretrieve("https://www.citeab.com/browse/suppliers","D:\pythonprojects\citeab.html")

#正则表达式
##pattern = re.compile(r'Hello')
##print(pattern)
##print(re.match(pattern,'hellohello',re.I))
##print('*************')
##print(re.search(pattern,'asdfashello'))
##print(re.split(pattern,'hello123hellosldflsdhello897'))
##r = re.split(pattern,'hello123hellosldflsdhello897')
##print(r[::3])

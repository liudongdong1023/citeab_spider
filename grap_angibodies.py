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
db = MySQLdb._mysql.connect("localhost","root","","citeab")
urllib.request.ProxyHandler({'https':('49.118.123.63','110.73.8.28','123.97.12.89','114.230.30.240','106.81.200.192','113.72.113.32')})
#遍历所有的供应商所在页面网址
sql = "select website from suppliers"
db.query(sql)

result = db.store_result()
 
print(db.affected_rows())
i = db.affected_rows()
while i:  
  tem_data  = result.fetch_row(1,1)
  data = tem_data[0]['website']
  data = data.decode()
  #请求网页
  responses = urllib.request.Request(data,None,{'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)','Referer':'https://www.citeab.com'})

  try:
    result1 = urllib.request.urlopen(responses)
  except urllib.error.HTTPError as e:
    print("HTTPError："+str(e.code))
  except urllib.error.URLError as e:
    print("URLError:"+e.reason)
content = result1.read().decode("utf-8")
print(content)
  #urllib.request.urlretrieve(data,"D:\pythonprojects\citeab1.html")




  

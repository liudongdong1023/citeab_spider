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

#https_proxy = ['63.149.98.170:80','63.149.98.23:80','63.149.98.43:80','117.143.109.158:80','35.154.255.215:80','199.195.119.37:80','34.249.20.9:3129','117.143.109.133:80','49.140.65.25:8998','175.45.187.5:8080']
for line in open('ips.txt'):
  print(line)
  proxy_support = urllib.request.ProxyHandler({'https': 'https://%s' % line})
  #proxy_support = urllib.request.ProxyHandler({'https': 'https://209.33.162.219:8080'})

  opener = urllib.request.build_opener(proxy_support)
  opener.addheaders = [('User-Agent' , 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'),('Referer','https://www.citeab.com')]
  urllib.request.install_opener(opener)

  sql = "select website,name from suppliers"
  db.query(sql)

  tem_i = 0
  result = db.store_result()
 
  print(db.affected_rows())
  if(tem_i == 0):
    i = db.affected_rows()
  else:
    i = tem_i
  while i:  
    tem_data  = result.fetch_row(1,1)
    data = tem_data[0]['website']
    supplier_name  = tem_data[0]['name']
    data = data.decode()
    supplier_name = supplier_name.decode()
    print(data)
    print(supplier_name)
    i = i - 1
    try:
      responses = opener.open(data)
    except urllib.error.HTTPError as e:
      print("HTTPError："+str(e.code))
      tem_i = i
      break
    except urllib.error.URLError as e:
      print("URLError:"+str(e.reason))
      tem_i = i
      break
content = responses.read().decode("utf-8")
  #print(content)
  #正则表达式提取内容
  #pattern = re.compile('<div class="search-result-row">.*?<div class="title-row">.*?<div class="ab-code-name">.*?<div class="ab-code">((.*?))</div>.*?<div class="ab-name">.*?<a href="(.*?)">(.*?)</a>.*?</div>.*?</div>.*?<div class="ab-cite">.*?<div class="ab-cite-inner radius">.*?<span>(.*?)</span>.*?<div class="col col01">.*?<div class="ab-supplier">.*?<div class="wrapper">(.*?)</div>.*?</div><div class="ab-host">.*?<dir class="wrapper">(.*?)</div>.*?</div><div class="ab-clone">.*?<div class="wrapper">(.*?)</div>.*?</div>.*?</div>.*?<div class="col col02">.*?<div class="ab-app">.*?<div class="wrapper">.*?<abbr class="app-abbr" title="Enzyme-linked immunosorbent assay ">(.*?)</abbr>.*?<div class="ab-react">.*?<div class="wrapper">.*?<ul class="reactant-summary">.*?<li>(.*?)</li>.*?</ul>')
  #pattern_supplier_name = re.compile('<div.*?class="wrapper">(.*?)</div>')
pattern_name = re.compile('<a.*?="/antibodies/.*?">(.*?)</a>')
items_supplier_name  = re.findall(pattern_name,content)
for item in items_supplier_name:
    print(item)
    sql1 = "insert into antibodys(supplier_name,name) values('%s','%s')" % (supplier_name,item)
    db.query(sql1)
  #获取分页地址，循环提取
pattern_name_pagination = re.compile('<a.*?="/search/page/(.*?)">.*?</a>')
items_name_pagination = re.findall(pattern_name_pagination,content)
for item in items_name_pagination:
    print(item)
    pagination_url = 'https://citeab.com/search/page/%s' % (item)
    print(pagination_url)
    try:
       responses = opener.open(pagination_url)
    except urllib.error.HTTPError as e:
      print("HTTPError："+str(e.code))
    except urllib.error.URLError as e:
      print("URLError:"+str(e.reason))
    content = responses.read().decode("utf-8")  
    pattern_name = re.compile('<a.*?="/antibodies/.*?">(.*?)</a>')
    items_supplier_name  = re.findall(pattern_name,content)
    for item in items_supplier_name:
        print(item)
        sql2 = "insert into antibodys(supplier_name,name) values('%s','%s')" % (supplier_name,item)
        db.query(sql2)
  

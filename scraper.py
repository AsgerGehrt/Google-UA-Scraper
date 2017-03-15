from lxml import html
from lxml import etree
import requests
import lxml
import re
import csv
import linecache
import config
from time import sleep


user_agent=config.user_agent



with open("sourcelist.csv", "r") as f:
	reader=csv.reader(f, delimiter=",")
	data=list(reader)
	row_count=len(data)
	print row_count
	
i=1

with open("output.csv", "wb") as fp:   #create output.csv
	a=csv.writer(fp, delimiter=";")
	data=[["URL", "User ID"]]
	a.writerows(data)
	fp.close()

for _ in range(row_count):	
	url="http://"+linecache.getline("sourcelist.csv", i).rstrip('\n')  
	headers = {"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"}
	#url="http://www.19min.bg"	

	print url
	try:
		page=requests.get(url, headers=headers, allow_redirects=True, timeout=10)
		#sleep(1)
		#print repr(page)
		#print page.headers
	except requests.exceptions.Timeout:
		i =i+1
		fields=[url,["TimeOut"]]
		with open ("output.csv", "ab") as o:
			writer=csv.writer(o)
			writer.writerows([fields])
		print "timeout"
		continue
	
	except requests.exceptions.ConnectionError: #HTTPSConnectionPool:
		i=i+1
		fields=[url, "URL not valid"]
		with open ("output.csv", "ab") as o:
			writer=csv.writer(o)
			writer.writerows([fields])
		print "URL not valid"
		continue
	
	except requests.exceptions.ContentDecodingError:
		i=i+1
		fields=[url, "Host server error"]
		with open ("output.csv", "ab") as o:
			writer=csv.writer(o)
			writer.writerows([fields])
		print "Host server error"
		continue
	#print page.content			
	try:	
		tree=html.fromstring(page.content)

	except lxml.etree.ParserError:
		#fields=[url, "Parser Error"]
		#with open ("output.csv", "ab") as o:
		#	writer=csv.writer(o)
		#	writer.writerows([fields])
		print "Parser Error, trying again"
		for page in page:	    
		
		#txt = etree.tostring(tree, pretty_print=True)
			uas = re.search('(UA-[0-9]*)', page)
		
			if uas is not None:			
								
				ua = uas.group(0)
				fields=[url,ua]
				with open ("output.csv", "ab") as o:
					writer=csv.writer(o)
					writer.writerows([fields])
				print ua
			#else: 
				#fields=[url, "nothing found"]
				#with open ("output.csv", "ab") as o:
				#	writer=csv.writer(o)
				#	writer.writerows([fields])
				#print fields
		i=i+1
		continue
	for tree in tree:	    
		
		txt = etree.tostring(tree, pretty_print=True)
		uas = re.search('(UA-[0-9]*)', txt)
		
		if uas is not None:			
			ua = uas.group(0)
			fields=[url,ua]
			with open ("output.csv", "ab") as o:
				writer=csv.writer(o)
				writer.writerows([fields])
			print ua
		else: 
			fields=[url, "nothing found"]
			with open ("output.csv", "ab") as o:
				writer=csv.writer(o)
				writer.writerows([fields])
			print fields

	#	if found==False:
	#		fields=[url,["N/A"]]
	#		with open ("output.csv", "ab") as o:
	#			writer=csv.writer(o)
	#			writer.writerows([fields])		
	#		print "not found"
	#		i=i+1		
	#		continue
	

	i=i+1
	
f.close()



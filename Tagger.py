import requests
import re
import os
import json
from bs4 import BeautifulSoup
def format_url(fileurl):
	tmpchr=""
	tmpchrs=""
	for chars in fileurl:
		if chars == '/':
			tmpchr = ""
		else:
			tmpchr+=chars
	for chars in tmpchr:
		if chars != '_':
			tmpchrs+=chars
		else:
			break
	return tmpchrs

def format_tags(html_doc):
	soup = BeautifulSoup(html_doc,"html.parser")
	print ("Getting Tags...")
	p_nodes = soup.find_all('tr')
	lists=[]
	for p_node in p_nodes:
		tag_now=p_node.get_text().strip()
		if tag_now[0] != 'G':
			if tag_now[0] != 'S':
				if tag_now[6] != ':':
					tmpstr=''
					for chars in tag_now:
						if chars != '\n':
							tmpstr+=chars
						else:
							break
					lists.append(tmpstr)
	return lists

def tag_query(fileurl):
	url = "http://kanotype.iptime.org:8003/deepdanbooru/upload"
	fl = open(fileurl,'rb')
	flee = format_url(fileurl)
	flag = 0
	for i in flee:
		if flag == 1:
			if i == 'p':
				flee = 'png'
				break
			elif i == 'j':
				flee = 'jpg'
				break
		if i == '.':
			flag = 1

	files = {'file': ('1.'+flee, fl, 'image/'+flee)}
	r2 = requests.post(url, data={"network_type": "general"}, files=files)
	return format_tags(r2.text)

def add_tag(fileurl):
	post_id = format_url(fileurl)
	print("Tagging to ",post_id)
	url = "https://example.com/api/post/" + post_id
	headers = {
            'Accept':'application/json',
            'Authorization':'',
            'Cookie':'',
            'Content-Type':'application/json'
			}
	payload = {
			"version":0,
			"tags":[""]
			}
	payload['tags'] = tag_query(fileurl)
	response = requests.put(url, data=json.dumps(payload), headers=headers)
	print(post_id,":",response)

rootdir = '/var/local/szurubooru/data/posts/'
list = os.listdir(rootdir)
for i in range(0,len(list)):
	print('Processing',i+1)
	path = os.path.join(rootdir,list[i])
	if os.path.isfile(path):
		add_tag(path)
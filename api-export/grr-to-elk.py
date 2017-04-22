#!/usr/bin/python
import urllib2
import ssl
import json
from elasticsearch import Elasticsearch

try:
  es = Elasticsearch(
      ['elk.blackhatsquirrel.com'],
      #http_auth=('YOUR_USERNAME', 'YOUR_PASSWORD'),
      port=9200,
  )
  print "Connected", es.info()
except Exception as ex:
  print "Error:", ex

ssl._create_default_https_context = ssl._create_unverified_context
SERVER = 'grr.blackhatsquirrel.com'
authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
authinfo.add_password(None, SERVER, 'apiadmin', 'tyghvb1122')
page = 'HTTPS://'+SERVER+'/api/hunts'
handler = urllib2.HTTPBasicAuthHandler(authinfo)
myopener = urllib2.build_opener(handler)
opened = urllib2.install_opener(myopener)
output = urllib2.urlopen(page)
printing = output.read()
## Remove the HTML header from response
stripped = printing[4:]
parsed_json = json.loads(stripped)
count_hunts = parsed_json['total_count']
#print "total numer of hunts is %s" %count_hunts
hunt_list=[]
for key in parsed_json["items"]:
	a = (key["value"]["urn"]["value"])
	## Strip AFF4 from response
	b = a[5:]
	hunt_list.append(b)
	#hunt_list.append((key["value"]["urn"]["value"]))
print hunt_list
for hunt_name in hunt_list:
	hunt_count_url = 'HTTPS://'+SERVER+'/api'+hunt_name+'/results?offset=1&count=1'
	#print hunt_count_url
	hunt_count_url_output = urllib2.urlopen(hunt_count_url)
	#print hunt_count_url_output
	hunt_count_read = hunt_count_url_output.read()
	#print hunt_count_read
	hunt_count_read_json = hunt_count_read[4:]
	hunt_count_parsed_json = json.loads(hunt_count_read_json)
	hunt_count_number = hunt_count_parsed_json['total_count']
	counter = 1
	while (counter < hunt_count_number):
	## DEBUG COUNTER
	#while (counter < 2):
		counter = counter + 1 
		#print counter
		counter_string = str(counter)
		hunt_return_url = 'HTTPS://'+SERVER+'/api'+hunt_name+'/results?offset='+counter_string+'&count=1'
		hunt_return_url_output = urllib2.urlopen(hunt_return_url)
		hunt_return_url_read = hunt_return_url_output.read()
		hunt_return_url_stripped = hunt_return_url_read[4:]
		hunt_return_parsed_json = json.loads(hunt_return_url_stripped)
		#print hunt_return_parsed_json
		for key in hunt_return_parsed_json["items"]:
			#print key
			es.index(index="grrpythontest-2", doc_type="grroutput", body=key)
		
## SOUNDTRACK - This script was hacked together while listening to Nothing but Thieves 
	


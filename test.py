import requests
import time
import json 

url = "https://gandalf.segmentify.com//add/events/v1.json?apiKey=7a149359-e360-4669-aa11-a2d8a9ecf0a6"

payload = "{\"async\": \"true\",\r\n\"browser\": \"Chrome\",\r\n\"category\": \"Category Page\",\r\n\"currency\": \"\",\r\n\"device\": \"PC\",\r\n\"email\": \"\",\r\n\"lang\": \"TR\",\r\n\"name\": \"PAGE_VIEW\",\r\n\"nextPage\": false,\r\n\"noProcess\": false,\r\n\"os\": \"Windows\",\r\n\"osversion\": \"10\",\r\n\"params\":{\"gender\":\"__ANY__\"},\r\n\"pageUrl\": \"https://www.watsons.com.tr/c/makyaj-281?pagenumber=2\",\r\n\"recommendIds\": [],\r\n\"referrer\": \"\",\r\n\"region\": \"\",\r\n\"sessionId\": \"7298412948190920704\",\r\n\"subCategory\": \"Makyaj\",\r\n\"testMode\": \"false\",\r\n\"tryCount\": 0,\r\n\"type\":\"widget-view\",\r\n\"tz\": \"-180\",\r\n\"userId\":\"2380481611291172865\",\r\n\"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36\",\r\n\"ft\":\"2020.10.29 13:04:11.792\"\r\n}"
headers = {
  'Content-Type': 'text/plain',
  'X-Sfy-Api-Key': '7a149359-e360-4669-aa11-a2d8a9ecf0a6',
  'Accept': '*/*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
  'Origin': 'https://www.watsons.com.tr',
  'Sec-Fetch-Site': 'cross-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.watsons.com.tr/',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Host': 'gandalf.segmentify.com'
}

response = requests.request("POST", url, headers=headers, data = payload,stream=True)

print(response.headers)
print(response.status_code)


#with open("out.txt", 'wb') as fd:
#  for chunk in response.iter_content(chunk_size=128):
#    fd.write(chunk)

time.sleep(5)
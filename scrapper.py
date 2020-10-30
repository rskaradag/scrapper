import requests
import urllib.request
import time
import json
import csv
import subprocess, sys,os

#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=0&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')
#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=50&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')

#3207 product





url=""

def fetch_watsons():
	#print(os.getcwd())
	#f = open("cmd", "r")
	#line=f.read()
	#print(line)
	#p = subprocess.Popen(["C:\\Program Files\\Git\\git-bash.exe", 
	            #  line], 
	            #  stdout=sys.stdout)
	#print(p.communicate())

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
	  'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
	}

	response = requests.request("POST", url, headers=headers, data = payload)
	print(response.headers['Content-Type'])

def fetch_gratis():

	output=[]
	line=[]
	k=0
	for i in range(100,3300,100):

		print(str(i))
		response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=100&No='+str(i-100)+'&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')
		data=json.loads(response.content)

		for product in data["resultsList"]["records"]:
			if "sku.grm_Campaignsearch" in product["records"][0]["attributes"]:
				r= requests.get('https://www.gratis.com/ccstoreui/v1/products?fields=id%2ClistPrices%2CchildSKUs.repositoryId%2CchildSKUs.listPrices&productIds=' + str(product["records"][0]["attributes"]["product.id"][0]))
				r.encoding
				d_product = json.loads(r.content)
				line.append(str(product["records"][0]["attributes"]["sku.grm_DynamicSearchText3"][0]) if "sku.grm_DynamicSearchText3" in product["records"][0]["attributes"] else "")
				line.append(str(product["records"][0]["attributes"]["product.id"][0]))
				line.append(str(product["records"][0]["attributes"]["sku.gr_EanUpc"][0]))
				line.append(str(product["records"][0]["attributes"]["sku.displayName"][0]))
				line.append(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"])
				line.append(str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]))
				line.append(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"])

				#print(str(product["records"][0]["attributes"]["sku.grm_DynamicSearchText3"][0]) +str(product["records"][0]["attributes"]["product.id"][0])+ str(product["records"][0]["attributes"]["sku.displayName"][0]) + " - " + str(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"]) + " - " + str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]) + "--->" + str(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"]))
			else:
				r.encoding
				line.append(" ")
				line.append(str(product["records"][0]["attributes"]["product.id"][0]))
				line.append(str(product["records"][0]["attributes"]["sku.gr_EanUpc"][0]))
				line.append(str(product["records"][0]["attributes"]["sku.displayName"][0]))
				line.append(product["records"][0]["attributes"]["sku.salePrice"][0])
				line.append(" ")
				line.append(0)
				#print(str(product["records"][0]["attributes"]["sku.displayName"][0]) +str(product["records"][0]["attributes"]["product.id"][0])+ "--->" + str(product["records"][0]["attributes"]["sku.salePrice"][0]))

			output.append(line)
			line=[]
			k=k+1


	with open('out.csv', 'w', newline='',encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(["Kampanya", "ProductId","Barkod", "Urun Adi","Liste Fiyati","Indirim","Satis Fiyati"])
		for item in output:
			#print(item)
			writer.writerow(item)

def main():
	print("hello")
	fetch_watsons()
	fetch_gratis()

if __name__ == '__main__':
	main()
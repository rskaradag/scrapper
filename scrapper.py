import requests
import urllib.request
import time
import json
import csv

#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=0&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')
#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=50&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')

#3207 product

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
			line.append(str(product["records"][0]["attributes"]["sku.displayName"][0]))
			line.append(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"])
			line.append(str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]))
			line.append(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"])

			#print(str(product["records"][0]["attributes"]["sku.grm_DynamicSearchText3"][0]) +str(product["records"][0]["attributes"]["product.id"][0])+ str(product["records"][0]["attributes"]["sku.displayName"][0]) + " - " + str(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"]) + " - " + str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]) + "--->" + str(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"]))
		else:
			r.encoding
			line.append(" ")
			line.append(str(product["records"][0]["attributes"]["product.id"][0]))
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
	writer.writerow(["Kampanya", "ProductId", "Urun Adi","Liste Fiyati","Indirim","Satis Fiyati"])
	for item in output:
		#print(item)
		writer.writerow(item)
import requests
import time
import json
import xlsxwriter
import decimal
import subprocess, sys,os
from datetime import date
from bs4 import BeautifulSoup

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=0&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')
#response = requests.get('https://www.gratis.com/ccstoreui/v1/search?N=3790920594&Nrpp=50&No=50&Nr=AND(product.active%3A1%2CNOT(sku.listPrice%3A0.000000))&Ns=')

def fetch_watsons():
	url = "https://www.watsons.com.tr/c/makyaj-281?pagenumber="
	#64
	output=[]
	line=[]
	for i in range(1,5):
		tmp_url=url + str(i)
		print(tmp_url)
		response = requests.get(tmp_url)
		data=response.content

		soup = BeautifulSoup(data, 'html.parser', fromEncoding='utf-8')

		products = soup.select(".product-box-container.border.rounded.p-1.pb-4.h-100")
		for item in products:
			_barcode="-"
			_productName=item.select(".productbox-desc.text-left.mb-1")[0].text.strip().split("\n")[2]
			#print("Brand: " + item.select(".productbox-desc.text-left.mb-1")[0].text.strip().split("\n")[0])
			#print("Model: " + item.select(".productbox-desc.text-left.mb-1")[0].text.strip().split("\n")[2])

			print(_productName)
			if item.select(".list-inline-item.product-box-old-price.text-site-medium-gray.roboto-regular"):
				_campaign="Var"
				_listPrice=item.select(".list-inline-item.product-box-old-price.text-site-medium-gray.roboto-regular")[0].text.strip().split(" ")[0]
				_discount="-"
				_salesPrice=item.select(".list-inline-item.product-box-price.text-site-pink.roboto-medium")[0].text.strip().split(" ")[0]
			else:
				_campaign="Yok"
				_listPrice=item.select(".list-inline-item.product-box-price.text-site-pink.roboto-medium")[0].text.strip().split(" ")[0]
				_discount="-"
				_salesPrice="-"

			if item.select(".product-box-has-no-stock.position-absolute.l-50.t-50.text-center.rubik-medium.text-white.p-2.rounded.border.border-white"):
				_stock=item.select(".static-text")[0].text.strip()
			else:
				_stock="STOKTA"

			line.append(_barcode)
			line.append(_campaign)
			line.append(_productName)
			line.append(_listPrice)
			line.append(_discount)
			line.append(_salesPrice)
			line.append(_stock)

			[x.encode('UTF8') for x in line]

			output.append(line)
			line=[]

	with xlsxwriter.Workbook('WatsonsDailyReport '+date.today().strftime("%d-%m-%Y")+'.xlsx') as workbook:
		workbook.encoding="utf-8"
		worksheet = workbook.add_worksheet()
		worksheet.write_row(0,0,["Barkod","Kampanya", "Urun Adi","Liste Fiyati","Indirim","Satis Fiyati","Stok"])
		for row_num, data in enumerate(output):
			row_num +=1
			worksheet.write_row(row_num, 0, data)

def fetch_gratis():
	output=[]
	line=[]
	k=0
	#3300
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
				line.append(str(product["records"][0]["attributes"]["sku.gr_EanUpc"][0]))
				line.append(product["records"][0]["attributes"]["sku.displayName"][0])
				line.append(decimal.Decimal(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"]))

				_discount=str(round(decimal.Decimal(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"])/(decimal.Decimal(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"]))*100,1))+"%"

				#line.append(str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]))
				line.append(_discount)
				line.append(decimal.Decimal(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"]))

				#print(str(product["records"][0]["attributes"]["sku.grm_DynamicSearchText3"][0]) +str(product["records"][0]["attributes"]["product.id"][0])+ str(product["records"][0]["attributes"]["sku.displayName"][0]) + " - " + str(d_product["items"][0]["listPrices"]["TurkeyPriceGroup"]) + " - " + str(product["records"][0]["attributes"]["sku.grm_Campaignsearch"][0]) + "--->" + str(d_product["items"][0]["listPrices"]["loyaltyTurkeyPriceGroup"]))
			else:
				r.encoding
				line.append("-")
				line.append(str(product["records"][0]["attributes"]["sku.gr_EanUpc"][0]))
				line.append(product["records"][0]["attributes"]["sku.displayName"][0])
				line.append(decimal.Decimal(product["records"][0]["attributes"]["sku.salePrice"][0]))
				line.append("-")
				line.append("-")
				#print(str(product["records"][0]["attributes"]["sku.displayName"][0]) +str(product["records"][0]["attributes"]["product.id"][0])+ "--->" + str(product["records"][0]["attributes"]["sku.salePrice"][0]))

			output.append(line)
			line=[]
			k=k+1

	with xlsxwriter.Workbook('GratisDailyReport '+date.today().strftime("%d-%m-%Y")+'.xlsx') as workbook:
		workbook.encoding="utf-8"
		worksheet = workbook.add_worksheet()
		worksheet.write_row(0,0,["Kampanya","Barkod", "Urun Adi","Liste Fiyati","Indirim","Satis Fiyati"])
		for row_num, data in enumerate(output):
			row_num +=1
			worksheet.write_row(row_num, 0, data)

def send_email():
	subject = "Gratis & Watsons Daily Report "+date.today().strftime("%d-%m-%Y")
	body = "This is an email with attachment sent from data collector service by RSK"
	sender_email = "automationinforsk@gmail.com"
	receiver_email = "gozde.uysal@eveshop.com.tr"
	password = "Gzdeuysal2"

	# Create a multipart message and set headers
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = subject
	#message["Bcc"] = receiver_email  # Recommended for mass emails

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	filename = 'GratisDailyReport '+date.today().strftime("%d-%m-%Y")+'.xlsx' # In same directory as script

	# Open PDF file in binary mode
	with open(filename, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
	    "Content-Disposition",
	    f"attachment; filename= {filename}",
	)

	# Add attachment to message and convert message to string
	message.attach(part)
	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, text)

def main():
	print("hello")
	fetch_watsons()
	fetch_gratis()
	send_email()

if __name__ == '__main__':
	main()
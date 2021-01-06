from bs4 import BeautifulSoup
import requests

#https://www.watsons.com.tr/c/makyaj-281?pagenumber=2

url = "https://www.watsons.com.tr/c/makyaj-281?pagenumber="
#64

for i in range(1,65):
  tmp_url=url + str(i)
  print(tmp_url)
  response = requests.get(tmp_url)

  data=response.content

  soup = BeautifulSoup(data, 'html.parser')

  products = soup.select(".product-box-container.border.rounded.p-1.pb-4.h-100")
  for item in products:
    #print("Brand: " + item.select(".productbox-desc.text-left.mb-1")[0].text.strip().split("\n")[0])
    print("Model: " + item.select(".productbox-desc.text-left.mb-1")[0].text.strip().split("\n")[2])
    if item.select(".mb-1"):
      print("Kampanya var")
    if item.select(".list-inline-item.product-box-old-price.text-site-medium-gray.roboto-regular"):
      print("Old Price: " + item.select(".list-inline-item.product-box-old-price.text-site-medium-gray.roboto-regular")[0].text.strip())
    #print("Price: " + item.select(".list-inline-item.product-box-price.text-site-pink.roboto-medium")[0].text.strip())
    print("-----------------------------------------------")







#parse_select(data)
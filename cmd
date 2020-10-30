cd C:\\Users\\rselc\\Desktop\\Works\\Scrapper\\scrapper
curl 'https://gandalf.segmentify.com//add/events/v1.json?apiKey=7a149359-e360-4669-aa11-a2d8a9ecf0a6' \
  -H 'Connection: keep-alive' \
  -H 'Accept: */*' \
  -H 'X-Sfy-Api-Key: 7a149359-e360-4669-aa11-a2d8a9ecf0a6' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36' \
  -H 'Content-Type: text/plain' \
  -H 'Origin: https://www.watsons.com.tr' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://www.watsons.com.tr/' \
  -H 'Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7' \
  --data-binary '[{"name":"PAGE_VIEW","userId":"2380481611291172865","sessionId":"7298412948190920704","testMode":"false","device":"PC","noProcess":false,"tryCount":0,"nextPage":false,"params":{"gender":"__ANY__"},"recommendIds":[],"pageUrl":"https://www.watsons.com.tr/c/makyaj-281?pagenumber=2","referrer":"","browser":"Chrome","os":"Windows","osversion":"10","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36","lang":"TR","currency":"","region":"","async":"true","email":"","ft":"2020.10.29 13:04:11.792","tz":"-180","category":"Category Page","subCategory":"Makyaj"}]' \
  --compressed > out.txt
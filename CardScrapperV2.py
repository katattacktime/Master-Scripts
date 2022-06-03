#reads card numbers from a file you create called cardlist.txt and then combines each number from each new line into a url that then automatically pulls from the CDN

from fake_useragent import UserAgent
import requests
import os
os.makedirs('CardScrapper', exist_ok=True)
os.makedirs('CardScrapper/card', exist_ok=True)
os.makedirs('CardScrapper/cutin', exist_ok=True)
os.makedirs('CardScrapper/cardstory', exist_ok=True)
os.makedirs('CardScrapper/usericon', exist_ok=True)

ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}

with open("cardlist.txt","r") as a_file:
	for line in a_file:
		line = line.replace('\n','')
		card = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/card/' + line)
		cutin = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/battle/cutin/card/' + line)
		cardstory = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/cardstory/cardstory_' + line)
		icon01 = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + line + '_01')
		icon02 = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + line + '_02')
		icon03 = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + line + '_03')
		icon04 = ('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + line + '_04')

		#card download
		r = requests.get(card, headers=header, allow_redirects=True)
		if r.status_code == 404:
			print('card ' + line + ' missing')
		else:
			open('CardScrapper/card/' + line, 'wb').write(r.content)
			print('card ' + line + ' downloaded.')

		#cutin download
		r = requests.get(cutin, headers=header, allow_redirects=True)
		if r.status_code == 404:
			()
		else:
			open('CardScrapper/cutin/' + 'cutin_' + line, 'wb').write(r.content)

		#cardstory download
		r = requests.get(cardstory, headers=header, allow_redirects=True)
		if r.status_code == 404:
			()
		else:
			open('CardScrapper/cardstory/' + 'cardstory_' + line, 'wb').write(r.content)

		#icons download
		#01
		r = requests.get(icon01, headers=header, allow_redirects=True)
		if r.status_code == 404:
			print('icon ' + line + ' missing')
		else:
			open('CardScrapper/usericon/' + line + '_01', 'wb').write(r.content)
			print('icon ' + line + ' downloaded')

		#02
		r = requests.get(icon02, headers=header, allow_redirects=True)
		if r.status_code == 404:
			()
		else:
			open('CardScrapper/usericon/' + line + '_02', 'wb').write(r.content)

		#03
		r = requests.get(icon03, headers=header, allow_redirects=True)
		if r.status_code == 404:
			()
		else:
			open('CardScrapper/usericon/' + line + '_03', 'wb').write(r.content)

		#04
		r = requests.get(icon03, headers=header, allow_redirects=True)
		if r.status_code == 404:
			()
		else:
			open('CardScrapper/usericon/' + line + '_04', 'wb').write(r.content)

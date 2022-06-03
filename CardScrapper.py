f=open('cards.txt', 'w')
with open("cardlist.txt","r") as a_file:
	for line in a_file:
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/card/' + line + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/battle/cutin/card/' + line + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/cardstory/cardstory_' + line + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + str(line)[:-1] + '_01' + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + str(line)[:-1] + '_02' + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + str(line)[:-1] + '_03' + '\n')
		f.write('https://cdn-seven.shall-we-date.com/AssetData/iOS/usericon/' + str(line)[:-1] + '_04' + '\n')


import os
from string import *
f=open('cards.txt', 'w')

for root, dirs, files in os.walk("."):
	for filename in files:
		if len(str(filename)) == 6 :
			f.write(str(filename) + '\n')
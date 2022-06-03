import os,sys

# folder = '' --- insert your folder here
for filename in os.listdir(folder):
	infilename = os.path.join(folder,filename)
	if not os.path.isfile(infilename): continue
	oldbase = os.path.splitext(filename)
	newname = infilename.replace('.bytes', '.psb')
	output = os.rename(infilename, newname)
import sys
import subprocess

def cmd(cmd):
	return subprocess.getoutput(cmd)

#labels
dirs = cmd("ls "+sys.argv[1])
labels = dirs.splitlines()

#make directries
cmd("mkdir images")

#copy images and make train.txt
pwd = cmd('pwd')
imageDir = pwd+"/images"
train = open('train.txt','w')
test = open('test.txt','w')
labelsTxt = open('labels.txt','w')
allimages = open('images.txt','w')

classNo=0
cnt = 0

for label in labels:
	workdir = pwd+"/"+sys.argv[1]+"/"+label
	imageFiles = cmd("ls "+workdir+"/*.jpg")
	images = imageFiles.splitlines()
	print(label)
	labelsTxt.write(label+"\n")
	startCnt=cnt
	length = len(images)
	for image in images:
		imagepath = imageDir+"/image%07d" %cnt +".jpg"
		cmd("cp "+image+" "+imagepath)
		if ((cnt-startCnt) % 11) != 0:
			train.write(imagepath+"\n")
		else:
			test.write(imagepath+"\n")
		cnt += 1
		allimages.write(imagepath+'\n')
	
	classNo += 1

train.close()
test.close()
labelsTxt.close()
allimages.close()

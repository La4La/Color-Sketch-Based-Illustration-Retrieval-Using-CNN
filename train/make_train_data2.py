import sys
import subprocess
import pandas as pd
import numpy as np


def cmd(cmd):
    return subprocess.getoutput(cmd)

#get labels
f = open('labels.txt','r')
data = f.read()
labels = data.split('\n')
f.close()
labels.pop()
labels

# folders
dirs = cmd("ls " + sys.argv[1])
folders = dirs.splitlines()

#copy images and make train.txt
pwd = cmd('pwd')
imageDir = pwd+"/images"

train_label = pd.DataFrame(np.zeros((900,len(labels)),dtype=np.float32),columns = labels)
test_label = pd.DataFrame(np.zeros((100,len(labels)),dtype=np.float32),columns = labels)

classNo = 0
cnt = 0
traincnt = 0
testcnt = 0
for folder in folders:
    workdir = pwd + "/" + sys.argv[1] + "/" + folder
    imageFiles = cmd("ls "+workdir+"/*.jpg")
    images = imageFiles.splitlines()
    print(folder)
    
    startCnt=cnt
    length = len(images)
    
    for image in images:
        imagepath = imageDir+"/image%07d" %cnt +".jpg"
        
        if ((cnt-startCnt) % 11) != 0:
            train_label.loc[traincnt,folder]=1
            traincnt += 1
        else:
            test_label.loc[testcnt,folder]=1
            testcnt += 1
        cnt += 1

    classNo += 1

train_label.to_csv('train_label.csv')
test_label.to_csv('test_label.csv')
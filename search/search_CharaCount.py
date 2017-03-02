import argparse
import random
import subprocess
import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean, hamming
from PIL import Image
import cv2

"""
Search similar illustrations according to user queries and count accuracy rates.
As an experiment, I tried 3 similarity comparation methods:
1. real number feature - Euclidean distance
2. binary feature - Hamming distance
3. binary feature - a new similarity defined by me
Result:
 When use a full connect layer for feature extraction, 3 is the best.
 When use an average pooling layer for feature extraction, 2 is the best.
"""

compares = {
    's': 'Similarity',
    'e': 'Euclidean distance',
    'h': 'Hamming distance'
    }

number_types = {
    'b': 'binary',
    'r': 'real number'
    }

parser = argparse.ArgumentParser(
    description='Similar illustration retrieval and accuracy counting')
parser.add_argument('directory', help='Path to inspection image file')
parser.add_argument('--model','-m',default='model', help='Path to model file')
parser.add_argument('--compare','-c',choices=compares.keys(),default='h',help='The way to compare')
parser.add_argument('--number_type','-n',choices=number_types.keys(),default='b',help='The number type of feature vector')
args = parser.parse_args()

def cmd(cmd):
    return subprocess.getoutput(cmd)

def read_image1(path, center=False, flip=False):
  cropwidth = 36 - model.insize
  image = np.asarray(Image.open(path)).transpose(2, 0, 1)
  image = image.astype(np.float32)
  if center:
    top = left = cropwidth / 2
  else:
    top = random.randint(0, cropwidth - 1)
    left = random.randint(0, cropwidth - 1)
  bottom = model.insize + top
  right = model.insize + left
  image = image[:, top:bottom, left:right].astype(np.float32)
  image /= 255
  if flip and random.randint(0, 1) == 0:
    return image[:, :, ::-1]
  else:
    return image

def read_image2(path, center=False, flip=False):
  img = cv2.imread(path)
  height, width, depth = img.shape
  output_side_length=32
  new_height = output_side_length
  new_width = output_side_length
  if height > width:
    new_height = output_side_length * height / width
  else:
    new_width = output_side_length * width / height
  resized_img = cv2.resize(img, (int(new_width), int(new_height)))
  height_offset = (new_height - output_side_length) / 2
  width_offset = (new_width - output_side_length) / 2
  cropped_img = resized_img[int(height_offset):int(height_offset + output_side_length),
  int(width_offset):int(width_offset + output_side_length)]
  image = np.asarray(cropped_img).transpose(2, 0, 1).astype(np.float32)
  image /= 255
  if flip and random.randint(0, 1) == 0:
    return image[:, :, ::-1]
  else:
    return image


#-------------------------------------------- load model --------------------------------------------
import densenet

model = densenet.DenseNet()
serializers.load_npz('trained_model', model)
model.to_cpu()

#-------------------------------------------- load vecs --------------------------------------------
if number_types[args.number_type] == 'real number':
    all = pd.read_csv("vec_real_number.csv", names=range(7168), dtype=np.float32)
else:
    all = pd.read_csv("vec_binary.csv", names=range(7168), dtype=np.int32)
    
    
#-------------------------------------------- prepare --------------------------------------------

# Indices of target illustrations
target = [67,86,160,146,248,267,348,335,451,407,572,562,622,669,741,783,805,816,922,965]
# Prepare to count the number which correctly searched
classNo_CharaCount = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 
                      11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}
top3_CharaCount = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 
                      11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}
top5_CharaCount = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 
                      11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}
top10_CharaCount = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 
                      11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0}


dirs = cmd("ls "+"dataset")
labels = dirs.splitlines()

pwd = cmd('pwd')

img_num = []
img_num.append(0)

for label in labels:
    workdir = pwd+"/"+"dataset"+"/"+label
    imageFiles = cmd("ls "+workdir+"/*.jpg")
    images = imageFiles.splitlines()

    img_num.append(len(images))

img_num = np.array(img_num)
end_num = np.cumsum(img_num)

imageDir = '/mnt/addhdd/gao/final/images_for_show/'


#------------------------------ 1st predict classNo (coarse-level search) ------------------------------

def main(directory, userDir, image):
    
    img = read_image1(directory+'/'+userDir+'/'+image)
    x = np.ndarray((1, 3, model.insize, model.insize), dtype=np.float32)
    x[0]=img
    x = chainer.Variable(np.asarray(x), volatile='on')

    score = model.inspection(x)
    score = np.array(score.data[0])
    classNo = score.argsort()[::-1][0]    

#------------------------------ 2nd abstract feature vector (fine-level search) ------------------------------

    img = read_image2(directory+'/'+userDir+'/'+image)
    x = np.ndarray((1, 3, model.insize, model.insize), dtype=np.float32)
    x[0]=img
    x = chainer.Variable(np.asarray(x), volatile='on')

    if number_types[args.number_type] == 'real number':
        vec = model.tovec_real(x)[0]
        vec = pd.DataFrame([vec], dtype=np.float32)
    else:
        vec = model.tovec_binary(x)[0]
        vec = pd.DataFrame([vec], dtype=np.int32)

#---------------------------------------- 3rd compare similarity ----------------------------------------

    classVec = all[end_num[classNo]:end_num[classNo+1]]

    compare = []

    #Use Euclidean distance (The smallest 5)
    if compares[args.compare] == 'Euclidean distance':
        for i in range(len(classVec)):    
            a=euclidean(classVec.iloc[i,:], vec.iloc[0,:])
            compare.append(a)

        compare = np.array(compare)

        top10 = compare.argsort()[:10]+end_num[classNo]

    elif compares[args.compare] == 'Hamming distance':
        for i in range(len(classVec)):    
            a=hamming(classVec.iloc[i,:], vec.iloc[0,:])
            compare.append(a)

        compare = np.array(compare)

        top10 = compare.argsort()[:10]+end_num[classNo]

    #Use similarity (The largest 5)
    else:
        for i in range(len(classVec)):    
            a=((classVec.iloc[i,:]==1)&(vec.iloc[0,:]==1)).sum()/(classVec.iloc[i,:]).sum()
            compare.append(a)

        compare = np.array(compare)

        top10 = compare.argsort()[::-1][:10]+end_num[classNo]
    
    rank = 1
    for j in top10:        
        cmd('cp '+imageDir+str(j)+'.jpg '+'search_result/'+userDir+'/'+image+'/'+str(rank)+'.'+str(j)+'.jpg')        
        rank += 1
    
    top5 = top10[:5]
    top3 = top5[:3]
    return(top3, top5, top10, classNo)




if __name__ == '__main__':
    
    cmd('mkdir search_result')
    
    directories = cmd('ls '+args.directory)
    D = directories.splitlines()
    
    for d in D:
        cmd('mkdir search_result/'+d)
        
        dirs = cmd('ls '+args.directory+'/'+d)
        images = dirs.splitlines()
        
        top3,top5,top10=0,0,0
        Num, RightPred = 0,0
        
        for i in images:
            cmd('mkdir search_result/'+d+'/'+i)

            result = main(args.directory,d,i)        

            if target[Num] in result[0]:
                top3 +=1
                top5 += 1
                top10 += 1
                top3_CharaCount[Num+1] += 1
                top5_CharaCount[Num+1] += 1
                top10_CharaCount[Num+1] += 1
            elif target[Num] in result[1]:
                top5 += 1
                top10 += 1
                top5_CharaCount[Num+1] += 1
                top10_CharaCount[Num+1] += 1
            elif target[Num] in result[2]:
                top10 += 1
                top10_CharaCount[Num+1] += 1
            
            RightChara = int(Num//2 == result[3])
            RightPred += RightChara
            classNo_CharaCount[Num+1] += RightChara
            
            Num += 1
            
        print(d,':',top3,',',top5,',',top10,'|',RightPred)
        
for i in range(1,21):
    print(i,':',top3_CharaCount[i],top5_CharaCount[i],top10_CharaCount[i],classNo_CharaCount[i])

#!/usr/bin/env python

from __future__ import print_function
import argparse
import random
import cv2
from PIL import Image
import numpy as np
import csv

parser = argparse.ArgumentParser(
    description='Save feature vectors')
parser.add_argument('image', help='Path to image file')
parser.add_argument('--model','-m',default='model', help='Path to model file')
args = parser.parse_args()

image = chainer.datasets.ImageDataset(args.image)

def read_image(image, center=False, flip=False):

  image = np.asarray(image).transpose(1, 2, 0).astype(np.float32)

  height, width, depth = image.shape
  output_side_length=32
  new_height = output_side_length
  new_width = output_side_length
  if height > width:
    new_height = output_side_length * height / width
  else:
    new_width = output_side_length * width / height
  resized_img = cv2.resize(image, (int(new_width), int(new_height)))
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

import densenet

model = densenet.DenseNet()
serializers.load_npz('trained_model', model)
model.to_cpu()

f = open('vec.csv', 'w')
writer = csv.writer(f, lineterminator='\n')

cnt = 1
all = len(image)

for i in range(len(image)): 
    
    print(cnt,'/',all)
    
    img = read_image(image[i])
    x = np.ndarray(
            (1, 3, model.insize, model.insize), dtype=np.float32)
    x[0]=img
    x = chainer.Variable(np.asarray(x), volatile='on')

    vec = model.predict(x)[0]
    writer.writerow(vec)
    
    cnt += 1

f.close()

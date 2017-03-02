import cv2
import argparse
import os
import numpy
import sys
import subprocess
 
parser = argparse.ArgumentParser(
    description='Image inspection using chainer')
parser.add_argument('directory', help='Path to inspection image file')
args = parser.parse_args()

def cmd(cmd):
    return subprocess.getoutput(cmd)

if __name__ == '__main__':
    cmd('mkdir query')
    
    directories = cmd('ls '+args.directory)
    D = directories.splitlines()
    
    for d in D:
        print(d)
        cmd('mkdir query/'+d)
        
        dirs = cmd('ls '+args.directory+'/'+d)
        images = dirs.splitlines()
        
        for i in images: 
            target_shape = (256, 256)

            imgpath = args.directory+'/'+d+'/'+i

            img = cv2.imread(imgpath)
            height, width, depth = img.shape
            output_side_length=256
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

            cv2.imwrite('query/'+d+'/'+i+".jpg", cropped_img) 
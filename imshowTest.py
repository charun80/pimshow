# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:54:11 2018

@author: Matthias Höffken
"""

imgDir = "/home/otto/Downloads/datasets/DaimlerBenchmark/SceneLabeling/train_1/imgleft"


from imshowViewer import ImageIteratorViewer
import threading
import time
import os
from glob import glob

import cv2
import numpy as np

img_list = glob(os.path.join( imgDir, '*.png'))
img_list.sort()


def imgIter( imgDir ):
    img_list = glob(os.path.join( imgDir, '*.png'))
    img_list.sort()
    
    while True:
        for path in img_list:
            img = cv2.imread( path )
            yield img.astype(np.uint8)


def main():
    
    app = ImageIteratorViewer( imgIter(imgDir), "ImageViewerTest" )
    #time.sleep(1)
    app.process()
    #app.start()
    #app.resizeViewer(1000,800)
    #
    #for img in imgIter(imgDir):
    #    time.sleep(1)
    #    app.addImage( np.empty((100,100,3), dtype=np.uint8) )
    #
    #app.join()    


if __name__ == '__main__':
    main()


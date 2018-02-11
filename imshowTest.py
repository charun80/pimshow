# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:54:11 2018

@author: Matthias Höffken
"""

imgDir = "/home/otto/Downloads/datasets/DaimlerBenchmark/SceneLabeling/train_1/imgleft"


from imshowApp import SimpleImageViewer
import threading
import time
import os
from glob import glob

import numpy as np

img_list = glob(os.path.join( imgDir, '*.png'))
img_list.sort()


def main():
    app = SimpleImageViewer("ImageViewerTest")
    #app.start()
    app.resizeViewer(1000,800)
    
    for i in range(10):
        time.sleep(1)
        app.addImage( np.empty((100,100,3), dtype=np.uint8) )
    
    app.join()    


if __name__ == '__main__':
    main()


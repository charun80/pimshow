# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 20:15:31 2018

@author: Matthias Höffken
"""

__all__ = ["ImageFrame"]

from PyQt5.QtGui import QImage, QPixmap
import numpy as np


class ImageFrame(object):
    
    mNpyImage = None
    mPixmapImage = None
    
    
    def __init__(self, npyImage):
        self.mNpyImage = npyImage
        qImage = self.toQImage( npyImage )
        self.mPixmapImage = QPixmap.fromImage( qImage )
    
    def getPixmapImage(self):
        return self.mPixmapImage

    @staticmethod
    def toQImage(img):
        
        if not np.issubdtype( img.dtype, np.uint8 ):
            raise TypeError( "dtype %r not supported" % img.dtype )
        
        height, width = img.shape[:2]
        nBytesPerLine = img.strides[0]
            
        if img.ndim == 2:
            qformat = QImage.Format_Grayscale8
        elif (img.ndim == 3) and (img.shape[2] in (3,4)):
            if img.shape[2] == 3:
                qformat = QImage.Format_RGB888
            elif img.shape[2] == 4:
                qformat = QImage.Format_ARGB32
        else:
            raise ValueError("shape %r not supported" % img.shape)
        
        qimg = QImage(img.data, width, height, nBytesPerLine, qformat)
        return qimg



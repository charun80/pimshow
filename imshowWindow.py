# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:13:23 2018

@author: Matthias Höffken
"""

__all__ = ["MainImshowWindow", "imshowFeature"]

from PyQt5.QtCore import pyqtSignal
from abstractImshowWindow import AbstractImshowWindow, imshowFeature
from imshowTools import ImageFrame

from enum import Enum, unique
from collections import deque



#@unique
#class viewerCommands(imshowFeature):
#    pass

viewerCommands = Enum('viewerCommands', \
                      [(i.name, i.value) for i in imshowFeature ] \
                      + [ ("FINISH", -1) ])


class MainImshowWindow(AbstractImshowWindow):
    newImageSignal = pyqtSignal(ImageFrame, name='newImage')
    resizeSignal = pyqtSignal( int, int, name='resize')
    
    
    mCurImage = None
    mCommandQueue = None
    
    
    def __init__(self, parent, optActions ):
        super(MainImshowWindow,self).__init__(parent, optActions)
        self.mCommandQueue = deque(maxlen=1)
        
        self.newImageSignal.connect( self.onNewImageAvailable )
        self.resizeSignal.connect( self.resize )
    
    
    def onNewImageAvailable(self, img ):
        self.mCurImage = img
        self.updateImage()
    
    
    def getCurrentImage(self):
        return self.mCurImage.getPixmapImage()
    
    
    def getCommandQueue(self):
        return self.mCommandQueue
    
    
    def triggerFinish(self):
        self.getCommandQueue().append( viewerCommands.FINISH )
    
    def triggerNext(self):
        self.getCommandQueue().append( viewerCommands.NEXT )
    
    def triggerPrev(self):
        self.getCommandQueue().append( viewerCommands.PREV )
    
    def triggerForwStartStop(self):
        self.getCommandQueue().append( viewerCommands.STARTSTOP )

    def triggerBackStartStop(self):
        self.getCommandQueue().append( viewerCommands.BACK_STARTSTOP )
    
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:13:23 2018

@author: Matthias Höffken
"""

__all__ = ["MainImshowWindow", "imshowFeature", "viewerResponse", "viewerCommands", "viewerErrors"]

from PyQt5.QtCore import pyqtSignal
from abstractImshowWindow import AbstractImshowWindow, imshowFeature
from imshowTools import ImageFrame

from enum import Enum, unique
from collections import deque



#@unique
#class viewerResponse(imshowFeature):
#    pass

viewerResponse = Enum('viewerResponse', \
                      [(i.name, i.value) for i in imshowFeature ] \
                      + [ ("OK", "Viewer state is ok"),
                          ("FINISHED", "Viewer is finished"),\
                          ("WINDOW_NOT_AVAILABLE", "ERROR: Viewer window seems not available (anymore)") ])


viewerCommands = frozenset( [ viewerResponse[m] for m in imshowFeature.__members__.keys() ] )
viewerErrors = frozenset([ viewerResponse.WINDOW_NOT_AVAILABLE ])




class MainImshowWindow(AbstractImshowWindow):
    newImageSignal = pyqtSignal(ImageFrame, name='newImage')
    resizeSignal = pyqtSignal( int, int, name='resize')
    
    
    mCurImage = None
    mResponseQueue = None
    
    
    def __init__(self, parent, optActions ):
        super(MainImshowWindow,self).__init__(parent, optActions)
        self.mResponseQueue = deque(maxlen=1)
        
        self.newImageSignal.connect( self.onNewImageAvailable )
        self.resizeSignal.connect( self.resize )
    
    
    def onNewImageAvailable(self, img ):
        self.mCurImage = img
        self.updateImage()
    
    
    def getCurrentImage(self):
        return self.mCurImage.getPixmapImage()
    
    
    def getResponseQueue(self):
        return self.mResponseQueue
    
    
    def triggerFinish(self):
        self.getResponseQueue().append( viewerResponse.FINISHED )
    
    def triggerNext(self):
        self.getResponseQueue().append( viewerResponse.NEXT )
    
    def triggerPrev(self):
        self.getResponseQueue().append( viewerResponse.PREV )
    
    def triggerForwStartStop(self):
        self.getResponseQueue().append( viewerResponse.STARTSTOP )

    def triggerBackStartStop(self):
        self.getResponseQueue().append( viewerResponse.BACK_STARTSTOP )
    
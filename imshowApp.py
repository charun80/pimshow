# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:46:06 2018

@author: Matthias Höffken
"""


__all__ = ["SimpleImageViewer"]


from imshowWindow import MainImshowWindow
from imshowTools import ImageFrame

from PyQt5.QtWidgets import QApplication



import threading
import numpy as np
#from enum import Enum, unique



class ImageViewerApplication(QApplication):
    
    appWindow = None

    def __init__(self, args ):
        QApplication.__init__(self, args)


    def startup(self, optActions):
        self.createWindow( optActions )

    def createWindow(self, optActions):
        self.appWindow = MainImshowWindow(self, optActions)
        self.appWindow.show()
    
    def destroyWindow(self):
        self.appWindow = None



class BaseImageViewer(threading.Thread):
    
    mViewerWindow = None
    mAppArgs = None
    
    mViewerWindowOpened = None
    mViewerWindowClosed = None
    
    mFrameCounter = None
    
    
    def __init__(self, ViewerName):
        super(BaseImageViewer, self).__init__()
        self.mAppArgs = [ViewerName]
        self.mOptActions = []
        self.mFrameCounter = 0
        
        self.mViewerWindowOpened = threading.Event()
        self.mViewerWindowOpened.clear()
        self.mViewerWindowClosed = threading.Event()
        self.mViewerWindowClosed.clear()    
    
    
    def __del__(self):
        self.join()


    def run(self):
        try:
            lApplication = ImageViewerApplication( self.mAppArgs )
            lApplication.startup( self.mOptActions )
            
            self.mViewerWindow = lApplication.appWindow
            self.mViewerWindowOpened.set()
            
            lApplication.exec_()
        finally:
            self.mViewerWindowClosed.set()
            self.mViewerWindowOpened.set()
            
            #self.mViewerWindow = None            
            #lApplication.destroyWindow()
            #lApplication = None
    
    
    def waitUntilAvailable(self, timeout = None):
        self.mViewerWindowOpened.wait( timeout )
        return ( not self.mViewerWindowClosed.is_set() )
    
    
    def isAvailable(self):
        return ( self.mViewerWindowOpened.is_set() and (not self.mViewerWindowClosed.is_set()) )
    
    
    def resizeViewer(self, width, height ):
        if self.isAvailable():
            self.mViewerWindow.resizeSignal.emit(width,height)
            return True
        else:
            return False
    
    
    def addImage(self, npyImg):
        img = ImageFrame( npyImg )
        
        if self.isAvailable():
            self.mFrameCounter += 1
            self.mViewerWindow.newImageSignal.emit(img)
            return True
        else:
            return False



class SimpleImageViewer(BaseImageViewer):

    def __init__(self, ViewerName):
        super(SimpleImageViewer, self).__init__(ViewerName)
        self.start()
        self.waitUntilAvailable()
    
    
    def runIterator( self, imgIter, delay=0 ):
        for img in imgIter:
            res = self.addImage( img )
            if not res:
                break
    
    
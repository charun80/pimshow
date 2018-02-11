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
from enum import Enum, unique



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
        

@unique
class ViewerState(Enum):
    NOT_STARTED = 0
    RUNNING     = 10
    FINISHED    = 100
    ERROR       = 200
    DESTROYED   = 1000



class BaseImageViewer(threading.Thread):
    
    mViewerWindow = None
    mAppArgs = None
    
    mViewerState = ViewerState.NOT_STARTED
    mFrameCounter = None
    
    
    def __init__(self, ViewerName):
        super(BaseImageViewer, self).__init__()
        self.mViewerState = ViewerState.NOT_STARTED
        self.mAppArgs = [ViewerName]
        self.mOptActions = []
        self.mFrameCounter = 0
    
    
    def __del__(self):
        self.join()


    def run(self):
        try:
            lApplication = ImageViewerApplication( self.mAppArgs )
            lApplication.startup( self.mOptActions )
            
            self.mViewerWindow = lApplication.appWindow
            self.mViewerState = ViewerState.RUNNING
            
            lApplication.exec_()
        except:
            self.mViewerState = ViewerState.ERROR
            raise
        finally:
            self.mViewerWindow = None
            if self.mViewerState is not ViewerState.ERROR:
                self.mViewerState = ViewerState.FINISHED
            
            lApplication.destroyWindow()
            lApplication = None
    
    
    def resizeViewer(self, width, height ):
        if self.mViewerState is ViewerState.RUNNING:
            self.mViewerWindow.resizeSignal.emit(width,height)
    
    
    def addImage(self, npyImg):
        img = ImageFrame( npyImg )
        
        if self.mViewerState is ViewerState.RUNNING:
            self.mFrameCounter += 1
            self.mViewerWindow.newImageSignal.emit(img)



class SimpleImageViewer(BaseImageViewer):

    
    
    def runIterator( self, imgIter, delay=0 ):
        pass
    
    
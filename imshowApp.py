# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:46:06 2018

@author: Matthias Höffken
"""


__all__ = ["SimpleImageViewer"]


from imshowWindow import MainImshowWindow, viewerCommands, viewerErrors, viewerResponse
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
    mViewerResponseQueue = None
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
            self.mViewerResponseQueue = self.mViewerWindow.getResponseQueue()
            assert( self.mViewerResponseQueue is not None )
            self.mViewerWindowOpened.set()
            
            lApplication.exec_()
        finally:
            self.mViewerWindowClosed.set()
            self.mViewerWindowOpened.set()
            
            #self.mViewerWindow = None            
            #lApplication.destroyWindow()
            #lApplication = None
    
    
    def waitUntilResponse(self, waitTime=0.1):
        while 0 == len(self.mViewerResponseQueue):
            time.sleep(waitTime)
        return self.mViewerResponseQueue.popleft()
    
    
    def waitUntilAvailable(self, timeout = None ):
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
            return viewerResponse.OK
        else:
            return viewerResponse.WINDOW_NOT_AVAILABLE




import time

viewerCommandsAndOk = viewerCommands.union( frozenset([viewerResponse.OK]) )


class SimpleImageViewer(BaseImageViewer):
    
    mImgIter = None
    
    
    def __init__(self, ViewerName, imgIter ):
        super(SimpleImageViewer, self).__init__(ViewerName)
        self.mImgIter = iter(imgIter)
        assert(not self.isAvailable())
        self.start()
        available = self.waitUntilAvailable()
        if not available:
            raise RuntimeError("Window %r is not available" % ViewerName)
        
    
    def __processIterator( self, delay ):
        
        tstart = time.clock()
        
        for img in self.mImgIter:
            vResp = self.addImage( img )

            if vResp is not viewerResponse.OK:
                return vResp
            
            while len(self.mViewerResponseQueue) > 0:
                vResp = self.mViewerResponseQueue.popleft()
                
                if vResp is viewerResponse.STARTSTOP:
                    return viewerResponse.OK
                else:
                    return vResp
            
            tRest = delay + tstart - time.clock()
            if tRest > 0:
                time.sleep(tRest)
            tstart = time.clock()
        
        return viewerResponse.FINISHED
        
    
    def process(self, start=False, delay=0 ):
        if start is True:
            vResp = viewerResponse.STARTSTOP
        else:
            vResp = viewerResponse.OK
        
        while vResp in viewerCommandsAndOk:
            
            # Wait for Signal
            if vResp is viewerResponse.OK:
                vResp = self.waitUntilResponse()
            
            # Single Image progress
            elif vResp is viewerResponse.NEXT:
                try:
                    img = self.mImgIter.next()
                except StopIteration:
                    return viewerResponse.FINISHED
                
                vResp = self.addImage( img )
            
            # Start video
            elif vResp is viewerResponse.STARTSTOP:
                
                vResp = self.__processIterator(delay)
            else:
                assert(False)
        
        return vResp
    
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 20:15:55 2018

@author: Matthias Höffken
"""


__all__ = ["ImageIteratorViewer"]

from imshowApp import ImageViewerThread
from imshowWindow import viewerCommands, viewerErrors, viewerResponse, imshowFeature
from imshowTools import ImageFrame



class BaseImageViewer(object):
    
    mViewerWindow = None    
    mViewerResponseQueue = None
    
    mFrameCounter = None
    
    
    def __init__(self, windowArgs):
        super(BaseImageViewer, self).__init__()
        self.mFrameCounter = 0
        
        viewerManager = ImageViewerThread.getInstance()
        self.mViewerWindow = viewerManager.createWindow( windowArgs )
        self.mViewerResponseQueue = self.mViewerWindow.getResponseQueue()
    
    
    def __del__(self):
        self.close()
        pass
    
    
    def close(self):
        if self.mViewerWindow is not None:
            self.mViewerWindow.close()
        self.mViewerWindow = None
        self.mViewerResponseQueue = None
    
    
    def waitUntilResponse(self, waitTime=0.01):
        while 0 == len(self.mViewerResponseQueue):
            time.sleep(waitTime)
        return self.mViewerResponseQueue.popleft()

    
    def resizeViewer(self, width, height ):
        self.mViewerWindow.resizeSignal.emit(width,height)
    
    
    def addImage(self, npyImg):
        # TODO: check if window is still available
        img = ImageFrame( npyImg )
        self.mViewerWindow.newImageSignal.emit(img)
        self.mFrameCounter += 1
        return viewerResponse.OK




import time

viewerCommandsAndOk = viewerCommands.union( frozenset([viewerResponse.OK]) )


class ImageIteratorViewer(BaseImageViewer):
    
    mImgIter = None
    
    
    def __init__(self, imgIter, WindowName ):
        super(ImageIteratorViewer, self).__init__([imshowFeature.NEXT, imshowFeature.STARTSTOP])
        self.mImgIter = iter(imgIter)
    
    
    def __showNextImage(self):
        for img in self.mImgIter:
            vResp = self.addImage( img )
            return vResp
        return viewerResponse.FINISHED
    
    
    def __processIterator( self, delay ):
        
        tstart = time.clock()
        
        while True:
            vResp = self.__showNextImage()
            
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
            vResp = self.__showNextImage()
        
        while vResp in viewerCommandsAndOk:
            
            # Wait for Signal
            if vResp is viewerResponse.OK:
                vResp = self.waitUntilResponse()
            
            # Single Image progress
            elif vResp is viewerResponse.NEXT:
                vResp = self.__showNextImage()
            
            # Start video
            elif vResp is viewerResponse.STARTSTOP:
                vResp = self.__processIterator(delay)
            
            else:
                assert(False)
        
        return vResp
    

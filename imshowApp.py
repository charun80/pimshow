# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:46:06 2018

@author: Matthias Höffken
"""


__all__ = ["ImageViewerThread"]


from imshowWindow import MainImshowWindow

from QtProxy import QApplication
from QtProxy import QtCore

import threading
from Queue import Queue
#import numpy as np
#from enum import Enum, unique

import sys
import traceback



class ImageViewerApplication(QApplication):
    # Here will be the singleton instance stored.
    __instance = None
    
    createWindowSignal = QtCore.Signal(tuple, name='createWindow')
    
    mWindowQueue = None
    
    
    def __init__(self, args ):
        """ Virtually private constructor. """
        QApplication.__init__(self, args)
        
        if ImageViewerApplication.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ImageViewerApplication.__instance = self    
        
        self.mWindowQueue = Queue()
        self.createWindowSignal.connect(self.__createNewWindow)

    @QtCore.Slot(tuple)
    def __createNewWindow(self, windowArgs):
        try:
            imshowWindow = MainImshowWindow(self, windowArgs)
            imshowWindow.show()
            self.mWindowQueue.put( imshowWindow )
        except:
            self.mWindowQueue( sys.exc_info() )
            traceback.print_exc()
            raise
    
    def getWindowQueue(self):
        return self.mWindowQueue



class ImageViewerThread(threading.Thread):
    
    # Here will be the singleton instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ImageViewerThread.__instance is None:
            ImageViewerThread()
        return ImageViewerThread.__instance
    
    
    mAppArgs = None
    mQapplicationCreated = None
    
    mWindowCreationSignal = None
    mWindowQueue = None
            
    
    def __init__(self):
        """ Virtually private constructor. """
        super(ImageViewerThread, self).__init__(target=self.__run)
        
        if ImageViewerThread.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ImageViewerThread.__instance = self        
        
        self.daemon = True
        self.mAppArgs = ["imshow"]
        self.mQapplicationCreated = threading.Event()
        self.mQapplicationCreated.clear()
        
        # start thread
        self.start()
        self.waitUntilAvailable()
    
    
    def __del__(self):
        self.join()


    def __run(self):
        
        lApplication = ImageViewerApplication( self.mAppArgs )
        # TODO: check how to handle no existing windows 
        #lApplication.setQuitOnLastWindowClosed( False )  # do not close in absense of windows
        
        self.mAppArgs = None
        self.mWindowQueue = lApplication.getWindowQueue()
        self.mWindowCreationSignal = lApplication.createWindowSignal
        
        self.mQapplicationCreated.set()
        
        lApplication.exec_()

    
    def waitUntilAvailable(self, timeout = None ):
        self.mQapplicationCreated.wait( timeout )
    
    
    def isAvailable(self):
        return self.mQapplicationCreated.is_set()
    
    
    def createWindow(self, windowArgs):
        if not isinstance( windowArgs, (tuple,list)):
            windowArgs = (windowArgs,)
        if isinstance( windowArgs, list ):
             windowArgs = tuple(windowArgs)
        
        self.waitUntilAvailable()
        self.mWindowCreationSignal.emit(windowArgs)
        
        response = self.mWindowQueue.get()
        if isinstance( response, tuple ) and (len(response) == 3):
            raise response[0], response[1], response[2]
        
        return response




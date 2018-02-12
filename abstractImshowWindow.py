# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:46:06 2018

@author: Matthias Höffken
"""

__all__ = ["AbstractImshowWindow", "imshowFeature" ]



from abc import ABCMeta, abstractmethod
from enum import Enum, unique

from imshowView import ImageView

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMenu, QFileDialog, QAction, QMessageBox


# Logging
import logging
Logger = logging.getLogger("abstractVisualizer")
Logger.setLevel("DEBUG")


@unique
class imshowFeature(Enum):
    NEXT = 1
    PREV = 2
    STARTSTOP = 3
    BACK_STARTSTOP = 4



class AbstractImshowWindow(QMainWindow):
    #__metaclass__ = ABCMeta
    
    # parameters
    auto_orient = True
    slide_delay = 5
    quality = 90    
    
    # Enum of available window actions
    mActions = None
    
    # dictionary of optional actions
    mOptActions = None
    
    # Signal Reactions and Widgets
    mExit = None
    mScene = None
    mImgView = None
    
    
    @abstractmethod
    def getCurrentImage(self):
        raise NotImplemented()
        
    
    
    def __init__(self, parent, optActions=[] ):
        QMainWindow.__init__(self)
        
        self.mOptActions = frozenset([ o for o in optActions if isinstance(o, imshowFeature) ])
        
        self.mExit = parent.closeAllWindows
        self.mScene = QGraphicsScene()
        
        self.mImgView = ImageView(self)
        self.mImgView.setScene(self.mScene)
        self.setCentralWidget(self.mImgView)

        self.create_actions()
        self.create_menu()
        #self.create_dict()
        #self.slides_next = True

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

        self.resize(700, 500)
    

    def create_actions(self):
        
        @unique
        class Actions(Enum):
            Save          = QAction('&Save image', self, shortcut='Ctrl+S')
            Close         = QAction('Close window', self, shortcut='Ctrl+W')
            Exit          = QAction('E&xit', self, shortcut='Ctrl+Q')
            ForwStartStop = QAction('Forward Start/Stop', self, shortcut='F5', checkable=True)
            BackStartStop = QAction('Backward Start/Stop', self, shortcut='F6', checkable=True)
            Next          = QAction('Next image', self, shortcut='Right')
            Prev          = QAction('Previous image', self, shortcut='Left')
            Fit           = QAction('Best &fit', self, checkable=True, shortcut='F')
            FScreen       = QAction('Fullscreen', self, shortcut='F11', checkable=True)
        
        Actions.Save.value.triggered.connect(self.saveImage)
        Actions.Close.value.triggered.connect(self.doClose)
        Actions.Exit.value.triggered.connect(self.doExit)
        Actions.FScreen.value.triggered.connect(self.toggleFullScreen)
        
        Actions.ForwStartStop.value.triggered.connect(self.triggerForwStartStop)
        Actions.BackStartStop.value.triggered.connect(self.triggerBackStartStop)
        Actions.Next.value.triggered.connect(self.triggerNext)
        Actions.Prev.value.triggered.connect(self.triggerPrev)
        Actions.Fit.value.triggered.connect(self.updateImage)
        Actions.Fit.value.setChecked(True)
        
        self.mActions = Actions
    
    
    def create_menu(self):
        self.popup = QMenu(self)
        
        # main_acts
        for opt,act in zip([ imshowFeature.NEXT, imshowFeature.PREV, imshowFeature.STARTSTOP, imshowFeature.BACK_STARTSTOP ],
                           [ self.mActions.Next, self.mActions.Prev, self.mActions.ForwStartStop, self.mActions.BackStartStop ]):
            
            if opt in self.mOptActions:
                self.popup.addAction(act.value)
                self.addAction(act.value)
            else:
                act = act.value
                act.setEnabled(False)
        
        view_acts = [ self.mActions.Fit, self.mActions.FScreen ]
        end_acts = [ self.mActions.Close, self.mActions.Exit ]
        
        for act in view_acts:
            self.popup.addAction(act.value)
            self.addAction(act.value)
            
        for act in end_acts:
            self.popup.addAction(act.value)
            self.addAction(act.value)

    
    
    def showMenu(self, pos):
        self.popup.popup(self.mapToGlobal(pos))



    ## Actions
    
    def updateImage(self):
        if self.mActions.Fit.value.isChecked():
            self.updateImageWithBestFit()
        else:
            self.updateImageWithOrigSize()
        
    
    def updateImageWithBestFit(self):
        """Update Image and fit to window"""
        image = self.getCurrentImage()
        if image is not None:
            self.mScene.clear()
            self.mScene.addPixmap(image)
            self.mScene.setSceneRect(0, 0, image.width(), image.height())
            self.mImgView.fitInView(self.mScene.sceneRect(), Qt.KeepAspectRatio)
    
    
    def updateImageWithOrigSize(self):
        """Load the image at its original size."""
        image = self.getCurrentImage()
        if image is not None:
            self.mScene.clear()
            self.mImgView.resetTransform()
            self.mScene.addPixmap(image)
            self.mScene.setSceneRect(0, 0, image.width(), image.height())
            pixitem = QGraphicsPixmapItem(image)
            self.mImgView.centerOn(pixitem)
    
    
    def doExit(self):
        try:
            self.triggerFinish()
        finally:
            self.mExit()
    
    def doClose(self):
        try:
            self.triggerFinish()
        finally:
            self.close()
    
    
    def triggerFinish(self):
        Logger.debug("triggerFinish::stub")
    
    def triggerNext(self):
        Logger.debug("triggerNext::stub")
    
    def triggerPrev(self):
        Logger.debug("triggerPrev::stub")
    
    def triggerForwStartStop(self):
        Logger.debug("triggerForwStartStop::stub")

    def triggerBackStartStop(self):
        Logger.debug("triggerBackStartStop::stub")


    def toggleFullScreen(self):
        if self.mActions.FScreen.value.isChecked():
            Logger.debug("toggleFullScreen::FullScreen")
            self.showFullScreen()
        else:
            Logger.debug("toggleFullScreen::Normal")
            self.showNormal()



    def saveImage(self):
        Logger.debug("save_img")
        fname = QFileDialog.getSaveFileName(self, 'Save your image')[0]
        if fname:
            if fname.lower().endswith(self.write_list):
                keep_exif = QMessageBox.question(self, 'Save exif data',
                        'Do you want to save the picture metadata?', QMessageBox.Yes |
                        QMessageBox.No, QMessageBox.Yes)
                if keep_exif == QMessageBox.Yes:
                    self.pixmap.save(fname, None, self.quality)
            else:
                QMessageBox.information(self, 'Error', 'Cannot save {} images.'.format(fname.rsplit('.', 1)[1]))

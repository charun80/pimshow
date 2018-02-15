# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 23:22:28 2018

@author: Matthias Höffken
"""

__all__ = [ \
    "QtCore", "QtGui", "Qt", "pyqtSignal", \
    "QApplication", "QMainWindow", "QGraphicsScene", "QGraphicsPixmapItem", "QMenu", \
    "QFileDialog", "QAction", "QMessageBox", "QGraphicsView", "QFrame", \
    "QImage", \
    "QImage2QPixmap_OutsideGui", "QImage2QPixmap_InsideGui" ]


USE_QT5 = True
USE_QT4 = False


if USE_QT5:
    try:
        
        from PyQt4 import QtCore
        from PyQt4 import QtGui
        
        QtCore.Signal = QtCore.pyqtSignal
        QtCore.Slot = QtCore.pyqtSlot
        
        from PyQt5.QtCore import Qt, pyqtSignal
        from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMenu, \
                                    QFileDialog, QAction, QMessageBox, QGraphicsView, QFrame
        
        from PyQt5.QtGui import QImage, QPixmap
        
        QImage2QPixmap_OutsideGui = lambda x: QPixmap.fromImage( x )
        QImage2QPixmap_InsideGui = lambda x: x
        
    except ImportError:
        USE_QT4 = True
    except RuntimeError:
        USE_QT4 = True


if USE_QT4:
    
    from PyQt4 import QtCore
    from PyQt4 import QtGui
        
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    
    
    from PyQt4.QtCore import Qt, pyqtSignal
    from PyQt4.QtGui import QApplication, QMainWindow, QGraphicsScene, QGraphicsPixmapItem, QMenu, \
                            QFileDialog, QAction, QMessageBox, QGraphicsView, QFrame
    
    from PyQt4.QtGui import QImage, QPixmap

    
    QImage2QPixmap_OutsideGui = lambda x: x
    QImage2QPixmap_InsideGui = lambda x: QPixmap.fromImage( x )

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:48:35 2018

@author: Matthias Höffken
"""

__all__ = ["ImageView"]


from QtProxy import Qt
from QtProxy import QGraphicsView, QFrame



class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.triggerPrev = parent.triggerPrev
        self.triggerNext = parent.triggerNext

        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(pal)
        self.setFrameShape(QFrame.NoFrame)

    def mousePressEvent(self, event):
        """Go to the next / previous image, or be able to drag the image with a hand."""
        if event.button() == Qt.LeftButton:
            x = event.x()
            if x < 100:
                self.triggerPrev()
            elif x > self.width() - 100:
                self.triggerNext()
            else:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.NoDrag)
        QGraphicsView.mouseReleaseEvent(self, event)

    def zoom(self, zoomratio):
        self.scale(zoomratio, zoomratio)

    def wheelEvent(self, event):
        zoomratio = 1.1
        if event.angleDelta().y() < 0:
            zoomratio = 1.0 / zoomratio
        self.scale(zoomratio, zoomratio)



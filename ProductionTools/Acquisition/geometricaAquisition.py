# -*- coding: utf-8 -*-
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL, Qt
from qgis.gui import QgsMapTool, QgsRubberBand, QgsAttributeDialog, QgsMapToolAdvancedDigitizing
from qgis.utils import iface
from qgis.core import QgsPoint, QgsFeature, QgsGeometry, QGis, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.gui import QgsMapMouseEvent
import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence, QCursor, QPixmap, QColor
from PyQt4.QtCore import QSettings

class GeometricaAcquisition(QgsMapToolAdvancedDigitizing):
    def __init__(self, canvas, iface, action):
        super(GeometricaAcquisition, self).__init__(canvas, None)
        self.iface=iface        
        self.canvas = canvas
        self.rubberBand = None
        self.snapCursorRubberBand = None
        self.initVariable()
        self.setAction(action)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
                
    def canvasPressEvent(self, e):
        pass
    
    def activate(self):
        if self.toolAction:
            self.toolAction.setChecked(True)
        self.free = False
        self.cur = QCursor(QPixmap(["18 13 4 1",
                                    "           c None",
                                    "#          c #FF0000",
                                    ".          c #FF0000",
                                    "+          c #1210f3",
                                    "                 ", 
                                    "   +++++++++++   ",
                                    "  +     #     +  ",
                                    " +      #      + ",
                                    "+       #       +",
                                    "+       #       +",
                                    "++#############++", 
                                    "+       #       +",
                                    "+       #       +",
                                    " +      #      +",
                                    "  +     #     +  ",
                                    "   +++++++++++   ",
                                    "                 ",]))
        self.canvas.setCursor(self.cur)

    def deactivate(self):
        if self.toolAction:
            self.toolAction.setChecked(False)
        if self is not None:
            QgsMapTool.deactivate(self)
   
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.initVariable()
        if event.key() == Qt.Key_Control:
            self.free = False
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.free = True
        if event.key() == Qt.Key_Backspace:
            if self.geometry:
                self.geometry.pop()
                geom = QgsGeometry.fromPolygon([self.geometry])
                self.qntPoint -= 1
                self.rubberBand.setToGeometry(geom, None)      
    
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(True)
            self.rubberBand = None
            self.rubberBand = self.createRubberBand()
        self.qntPoint = 0
        self.geometry = []
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
    
    def lineIntersection(self, p1, p2, p3, p4):        
        m1 = (p1.y() - p2.y())/(p1.x() - p2.x())
        a1 = p2.y() + p2.x()/m1
        m2 = (p3.y() - p4.y())/(p3.x() - p4.x())
        #Reta perpendicular P3 P4 que passa por P4
        a2 = p4.y() + p4.x()/m2
        if abs(m1 - m2) > 0.01:
            #intersecao
            x = (a2 - a1)/(1/m2 - 1/m1) 
            y = -x/m1 + a1
            return QgsPoint(x,y)
        return False
    
    def projectPoint(self, p1, p2, p3):        
        #reta P1 P2
        try:
            a = (p2.y()-p1.y())/(p2.x()-p1.x())
            #reta perpendicular a P1P2 que passa por P2
            a2 = -1/a
            b2 =  p2.y() - a2*p2.x()
            #reta paralela a P1P2 que passa por P3
            b3 = p3.y() - a*p3.x()
            #intersecao entre retas
            x = (b3 - b2)/(a2 - a)
            y = a*x + b3
        except:
            return None

        return QgsPoint(x, y)
    
    def getRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, True)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        return rubberBand
    
    def getSnapRubberBand(self):
        rubberBand = QgsRubberBand(self.canvas, geometryType = QGis.Point)
        rubberBand.setFillColor(QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QColor(255, 0, 0, 200))
        rubberBand.setWidth(2)
        rubberBand.setIcon(QgsRubberBand.ICON_X)
        return rubberBand        
    
    def createGeometry(self, geom):
        geom = self.reprojectRubberBand(geom)
        if geom :
            layer = self.canvas.currentLayer()
            feature = QgsFeature()
            fields = layer.pendingFields()
            feature.setGeometry(geom)
            feature.initAttributes(fields.count())            
            provider = layer.dataProvider()              
            for i in range(fields.count()):
                feature.setAttribute(i, provider.defaultValue(i))                
            form = QgsAttributeDialog(layer, feature, False)
            form.setIsAddDialog(True)
            if not form.dialog().exec_():
                ok = False
            else:
                ok = True
            if ok:
                feature.setAttributes(form.feature().attributes())
                layer.endEditCommand()
                self.initVariable()    
            else:
                self.initVariable()   

    def createSnapCursor(self, point):
        self.snapCursorRubberBand = self.getSnapRubberBand()
        self.snapCursorRubberBand.addPoint(point) 
 
    def reprojectRubberBand(self, geom):
        """
        Reprojects the geometry
        geom: QgsGeometry
        """
        # Defining the crs from src and destiny
        epsg = self.canvas.mapSettings().destinationCrs().authid()
        crsSrc = QgsCoordinateReferenceSystem(epsg)
        #getting srid from something like 'EPSG:31983'
        layer = self.canvas.currentLayer()
        srid = layer.crs().authid()
        crsDest = QgsCoordinateReferenceSystem(srid) #here we have to put authid, not srid
        # Creating a transformer
        coordinateTransformer = QgsCoordinateTransform(crsSrc, crsDest)
        # Transforming the points
        poly = geom.asPolygon()
        newPolyline = []
        for j in xrange(len(poly)):
            line = poly[j]
            for i in xrange(len(line)):
                point = line[i]
                newPolyline.append(coordinateTransformer.transform(point))
        qgsPolygon = QgsGeometry.fromPolygon([newPolyline])                
        return qgsPolygon    
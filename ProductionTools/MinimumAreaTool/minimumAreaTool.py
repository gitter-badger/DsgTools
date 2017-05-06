# -*- coding: utf-8 -*-
"""
/***************************************************************************
MinimumAreaTool
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
                                            Felipe Diniz - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import QSettings, pyqtSignal, pyqtSlot, SIGNAL, QObject
from PyQt4.Qt import QWidget, QObject

#qgis imports
import qgis.utils
from qgis.gui import QgsMessageBar
#DsgTools Imports
from DsgTools.ProductionTools.MinimumAreaTool.shapeTool import ShapeTool
from DsgTools.ProductionTools.MinimumAreaTool.customSizeSetter import CustomSizeSetter

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'minimumAreaTool.ui'))

class MinimumAreaTool(QWidget,FORM_CLASS):
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
        super(MinimumAreaTool, self).__init__(parent)
        self.setupUi(self)
        self.splitter.hide()
        self.iface = iface
        self.mScaleWidget.setScaleString('1:100000')
        self.scale = None
        self.shape = None
        self.size = None
        self.populateSizesComboBox()
    
    def initGui(self):
        """
        Adds the tool bar in QGIS
        """
        self.iface.addToolBarWidget(self.splitter)
        
    def createDict(self, customDict = None):
        """
        Creates the dictionary used to create the geometry templates
        """
        self.sizes = {}
        self.sizes[u"25mm²"] = {'value': 25, 'shape': 'area'}
        self.sizes[u"4mm²"] = {'value': 4, 'shape': 'area'}
        self.sizes[u"1x1mm²"] = {'value': 1, 'shape': 'area'}
        self.sizes[u"0.8x0.8mm²"] = {'value': 0.64, 'shape': 'area'}
        self.sizes[u"0.8mm"] = {'value': 0.8,'shape': 'distance'}
        if customDict:
            for key in customDict:
                self.sizes[key] = customDict[key]
        
    def shapeComboSetter(self):
        """
        Sets the correct index for the shapes combo box according to the text select in the sizes combo box
        """
        if self.sizesComboBox.currentText() in self.sizes.keys():
            if self.sizes[self.sizesComboBox.currentText()]['shape'] == 'distance':
                #In this case we should force the use of circle, due to the measurement shape = distance and set the shape combo box enabled(False)
                self.shapesComboBox.setCurrentIndex(2)
                self.shapesComboBox.setEnabled(False)
            else:
                self.shapesComboBox.setEnabled(True)
        else:
            self.shapesComboBox.setEnabled(True)
    
    @pyqtSlot(int)
    def on_sizesComboBox_currentIndexChanged(self):
        """
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        """
        if self.sizesComboBox.currentIndex() <> 0:
            self.shapeComboSetter()
    
    @pyqtSlot(int)
    def on_shapesComboBox_currentIndexChanged(self):
        """
        Slot used to check if the user selected 0.8mm (this is used for linear features).
        In this case we should force the use of circle and set the shape combo box enabled(False)
        """
        if self.shapesComboBox.currentIndex() <> 0:
            self.shapeComboSetter()
    
    @pyqtSlot(bool)
    def on_drawShape_clicked(self):
        """
        Draws the select template shape on the map canvas
        """
        scaleText = self.mScaleWidget.scaleString()
        scale = int(scaleText.split(':')[-1].replace('.',''))/1000
        size = self.sizesComboBox.currentText()
        shape = self.shapesComboBox.currentText()
        validated = self.validateCombos(self.sizesComboBox.currentIndex(), self.shapesComboBox.currentIndex())
        if validated:
            crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
            if crs.mapUnits() == 2:
                self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('This tool does not work with angular unit reference system!'), level=QgsMessageBar.WARNING, duration=3)
            else:
                self.run(scale, size, shape)
        else:
            QMessageBox.warning(self.iface.mainWindow(), self.tr(u"Error!"), self.tr(u"<font color=red>Shape value not defined :</font><br><font color=blue>Define all values to activate tool!</font>"), QMessageBox.Close)              
    
    def run(self, scale, size, shape):
        """
        Runs the ShapeTool and set it as the current map tool
        """
        #checking the selected type
        if (self.sizes[size]['shape'] == 'area'):
            param = (float(scale)**2)*float(self.sizes[size]['value'])
        else:
            param = float(scale)*float(self.sizes[size]['value'])
        color = self.mColorButton.color()
        color.setAlpha(63)
        tool = ShapeTool(self.iface.mapCanvas(), shape, param, self.sizes[size]['shape'], color )
        tool.toolFinished.connect(self.refreshCombo)
        self.iface.mapCanvas().setMapTool(tool)

    def refreshCombo(self):
        """
        Re-enables the shapes combo
        """
        self.shapesComboBox.setEnabled(True)
    
    def validateCombos(self,size,shape):
        """
        Checks if all combos correctly selected
        """
        if size <> 0 and shape <> 0:
            return True
        else:
            return False

    @pyqtSlot(bool)
    def on_showPushButton_toggled(self, toggled):
        """
        Slot to show/hide the tool bar
        """
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()
    
    def getCustomSizesDict(self):
        #get custom sizes from qsettings
        settings = QSettings()
        settings.beginGroup('DSGTools/CustomSizes/')
        currentSettings = settings.childGroups()
        settings.endGroup()
        customSizesDict = dict()
        #get each parameter
        for settingName in currentSettings:
            customSizesDict[settingName] = dict()
            settings = QSettings()
            settings.beginGroup('DSGTools/CustomSizes/'+settingName)
            customSizesDict[settingName]['shape'] = settings.value('shape')
            customSizesDict[settingName]['value'] = settings.value('value')
            settings.endGroup()
        return customSizesDict
    
    def addValueToCustomSizesDict(self, newValueDict):
        settings = QSettings()
        if not settings.contains('DSGTools/CustomSizes/'+newValueDict['comboText']+'/shape'):
            settings.beginGroup('DSGTools/CustomSizes/'+newValueDict['comboText'])
            settings.setValue('shape', newValueDict['shape'])
            settings.setValue('value', newValueDict['value'])
            settings.endGroup()
        self.populateSizesComboBox()
    
    def populateSizesComboBox(self):
        self.sizesComboBox.clear()
        self.sizesComboBox.addItem(self.tr('SIZES'))
        self.sizesComboBox.addItem(u'25mm²')
        self.sizesComboBox.addItem(u'4mm²')
        self.sizesComboBox.addItem(u'0.8x0.8mm²')
        self.sizesComboBox.addItem(u'1x1mm²')
        self.sizesComboBox.addItem(u'0.8mm')
        customSizesDict = self.getCustomSizesDict()
        self.createDict(customDict = customSizesDict)
        self.populateComboWithCustomSizes(customSizesDict)
    
    def populateComboWithCustomSizes(self, customSizesDict):
        """
        Add to sizesComboBox values from customSizesDict and adds values to self.sizes 
        """
        for size in customSizesDict.keys():
            #add item to comboBox
            self.sizesComboBox.addItem(size)

    @pyqtSlot(bool)
    def on_createCustomSizesPushButton_clicked(self):
        """
        Opens custom size setter
        """
        customSizesDict = self.getCustomSizesDict()
        dlg = CustomSizeSetter(customSizesDict)
        dlg.sizeCreated.connect(self.addValueToCustomSizesDict)
        dlg.exec_()
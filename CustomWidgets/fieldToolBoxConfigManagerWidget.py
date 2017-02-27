# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog

#DsgTools imports
from DsgTools.ServerManagementTools.fieldToolBoxConfigManager import FieldToolBoxConfigManager
from DsgTools.CustomWidgets.genericParameterSetter import GenericParameterSetter
from DsgTools.CustomWidgets.genericManagerWidget import GenericManagerWidget
from DsgTools.CustomWidgets.listSelector import ListSelector
from DsgTools.ProductionTools.FieldToolBox.field_setup import FieldSetup
from DsgTools.Utils.utils import Utils

from qgis.core import QgsMessageLog
import json

class FieldToolBoxConfigManagerWidget(GenericManagerWidget):
    def __init__(self, manager = None, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(genericDbManager = manager, parent = parent)

    def setParameters(self, serverAbstractDb, dbsDict = {}):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.genericDbManager = FieldToolBoxConfigManager(serverAbstractDb, dbsDict)
            self.refresh()
        else:
            self.setComponentsEnabled(False)

    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = GenericParameterSetter()
        dlg.exec_()
        edgvVersion, propertyName = dlg.getParameters()
        if edgvVersion == self.tr('Select EDGV Version'):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Enter a EDGV Version'))
            return
        if propertyName == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Enter a Field Toolbox Configuration Name!'))
            return
        if propertyName in self.genericDbManager.getPropertyPerspectiveDict('property').keys():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Field Toolbox Configuration Name already exists!'))
            return
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        fieldDlg = FieldSetup(templateDb,returnDict = True)
        ret = fieldDlg.exec_()
        if ret == 1:
            fieldSetupDict = fieldDlg.makeReclassificationDict()
            self.genericDbManager.createSetting(propertyName,edgvVersion,fieldSetupDict)
            self.refresh()

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        availableConfig = self.genericDbManager.getPropertyPerspectiveDict().keys()
        dlg = ListSelector(availableConfig,[])
        dlg.exec_()
        selected = dlg.getSelected()
        if selected == []:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select at least one configuration!'))
            return
        for config in availableConfig:
            try:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                self.genericDbManager.installFieldToolBoxConfig(config)
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self, self.tr('Success!'), self.tr('Field Toolbox config ') + config + self.tr(' successfully installed.'))
                self.refresh()
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem applying field toolbox config: ') + e.args[0])
    
    @pyqtSlot(bool)
    def on_deleteCustomizationPushButton_clicked(self):
        #TODO: Reimplement
        customizationName = self.customizationListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete customization ')+customizationName+'?', QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.deleteCustomization(customizationName, edgvVersion)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customization ') + customizationName + self.tr(' successfully deleted.'))
            self.refreshProfileList()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem deleting customization: ') + e.args[0])
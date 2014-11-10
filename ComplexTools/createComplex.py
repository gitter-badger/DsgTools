# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtXml import *

from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery

from ui_createComplex import Ui_Dialog

class CreateComplexDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        QObject.connect(self.filePushButton, SIGNAL(("clicked()")), self.setFile)
        QObject.connect(self.fileLineEdit, SIGNAL(("editingFinished()")), self.loadDb)
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged (int)"), self.updateTableView)
        
        QObject.connect(self.selectAllButton, SIGNAL(("clicked()")), self.selectAllFeatures)
        QObject.connect(self.selectOneButton, SIGNAL(("clicked()")), self.selectOneFeature)
        QObject.connect(self.deselectOneButton, SIGNAL(("clicked()")), self.deselectOneFeature)
        QObject.connect(self.deselectAllButton, SIGNAL(("clicked()")), self.deselectAllFeatures)
        
        self.populateSelectedFeaturesWidget()
        
    def setFile(self):
        fd = QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.fileLineEdit.setText(self.filename)
            
        self.loadDb()

    def loadDb(self):
        self.filename = self.fileLineEdit.text()
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.filename)
        self.db.open()
        
        self.populateComboBox()
        
    def updateTableView(self):
        table = self.comboBox.currentText()
        
        projectModel = QSqlQueryModel()
        projectModel.setQuery("select * from "+table,self.db)
        
        self.tableView.setModel(projectModel)
        self.tableView.show()
        
    def populateComboBox(self):
        self.comboBox.clear()
        
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
        while query.next():
            name = query.value(0)
            if 'Complexo' in name:
                self.comboBox.addItem(query.value(0))

    def populateSelectedFeaturesWidget(self):
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue
            item = QTreeWidgetItem(self.selectedFeaturesTreeWidget)
            item.setText(0,layer.name())
            for feature in selectedFeatures:
                featureItem = QTreeWidgetItem(item)
                featureItem.setText(0,str(feature.id()))
                
    def selectAllFeatures(self):
        pass
    
    def selectOneFeature(self):
        pass

    def deselectOneFeature(self):
        pass

    def deselectAllFeatures(self):
        pass
    
# -*- coding: utf-8 -*-
"""
/***************************************************************************
 layerVersion
                                 A QGIS plugin
 layerVersion
                              -------------------
        begin                : 2014-09-24
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
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
from PyQt4.QtXml import *
from qgis.core import *
from functools import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from layerversiondialog import layerVersionDialog

from getlayeredits import getLayerEdits
from setlayeredits import setLayerEdits
import os.path


class trace:

    def __init__(self):
        self.trace = None
        
    def ce(self,string):
        if self.trace:
            print string

class layerVersion:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'layerversion_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = layerVersionDialog()
        self.tra = trace()
        self.editingStateLoader = setLayerEdits(self.iface)
        self.editingStateSaver = getLayerEdits(self.iface)
        
    def initGui(self):
        self.actionSave = QAction(
            QIcon(":/plugins/layerversion/save.png"),
            u"Save layers version", self.iface.mainWindow())
        self.actionSave.triggered.connect(self.save)
        self.actionLoad = QAction(
            QIcon(":/plugins/layerversion/load.png"),
            u"Load layers version", self.iface.mainWindow())
        self.actionLoad.triggered.connect(self.load)
        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionSave)
        self.iface.addPluginToVectorMenu(u"&layerVersion", self.actionSave)
        self.iface.addToolBarIcon(self.actionLoad)
        self.iface.addPluginToVectorMenu(u"&layerVersion", self.actionLoad)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginVectorMenu(u"&layerVersion", self.actionSave)
        self.iface.removeToolBarIcon(self.actionSave)
        self.iface.removePluginVectorMenu(u"&layerVersion", self.actionLoad)
        self.iface.removeToolBarIcon(self.actionLoad)



    # run method that performs all the real work
    def save(self):
        if self.iface.editableLayers():
            fileName = QFileDialog.getSaveFileName(None,"Save Qgis LayerEditsVersion definition", QgsProject.instance().readPath("./"), "*.qlv");
            self.tra.ce(fileName)
            if fileName:
                DOM = self.editingStateSaver.getEditsXMLDefinition()
                if DOM:
                    outFile = open(fileName, "w")
                    outFile.write(DOM.toString().encode('utf-8'))
                    outFile.close
        else:
            QMessageBox.critical(None, "Alert", "No Layers in Editing mode, No version to save")


    def load(self):
        #if self.iface.editableLayers():
        fileName = QFileDialog.getOpenFileName(None,"Open Qgis LayerEditsVersion definition", QgsProject.instance().readPath("./"), "*.qlv");
        if fileName:
            self.editingStateLoader.setEditsXMLDefinition(fileName)
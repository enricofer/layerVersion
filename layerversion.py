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
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from layerversiondialog import layerVersionDialog

from getlayeredits import getLayerEdits
from setlayeredits import setLayerEdits
import os.path

class trace:

    def __init__(self):
        self.trace = True
        
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

    def initGui(self):
        self.actionSave = QAction(
            QIcon(":/plugins/layerversion/icon1.png"),
            u"Save", self.iface.mainWindow())
        self.actionSave.triggered.connect(self.save)
        self.actionLoad = QAction(
            QIcon(":/plugins/layerversion/icon2.png"),
            u"Load", self.iface.mainWindow())
        self.actionLoad.triggered.connect(self.load)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.actionSave)
        self.iface.addPluginToMenu(u"&layerVersion", self.actionSave)
        self.iface.addToolBarIcon(self.actionLoad)
        self.iface.addPluginToMenu(u"&layerVersion", self.actionLoad)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&layerVersion", self.actionSave)
        self.iface.removeToolBarIcon(self.actionSave)
        self.iface.removePluginMenu(u"&layerVersion", self.actionLoad)
        self.iface.removeToolBarIcon(self.actionLoad)



    # run method that performs all the real work
    def save(self):
        editingState = getLayerEdits(self.iface)
        outFile = open(os.path.join(self.plugin_dir,"versions","LayerEdits.xml"), "w")
        outFile.write(editingState.getEditsXMLDefinition(self.iface.legendInterface().currentLayer()).toString(2))
        outFile.close
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            #pass


    def load(self):
        editingState = setLayerEdits(self.iface)
        self.tra.ce(editingState.setEditsXMLDefinition(os.path.join(self.plugin_dir,"versions","LayerEdits.xml")).toxml())
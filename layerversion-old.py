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

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/layerversion/icon.png"),
            u"layerVersion", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&layerVersion", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&layerVersion", self.action)
        self.iface.removeToolBarIcon(self.action)

    def getSavedFeaturesDom(self,XMLdoc,QFeatMap):
        self.tra.ce("XML00")
        self.tra.ce(QFeatMap)
        XMLaddedFeatures = QDomElement()
        XMLaddedFeatures = XMLdoc.createElement("ADDEDFEATURES")
        for QId, QFeat in QFeatMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QFeat)
            XMLAddedFeat = QDomElement()
            XMLAddedFeat = XMLdoc.createElement("FEAT")
            #XMLAddedFeat.setAttribute('id',QFeatMap.key())
            XMLAddedFeatID = QDomElement()
            XMLAddedFeatID = XMLdoc.createElement("ID")
            XMLAddedFeatGEOM = QDomElement()
            XMLAddedFeatGEOM = XMLdoc.createElement("GEOMETRY")
            XMLAddedFeatATTRS = QDomElement()
            XMLAddedFeatATTRS = XMLdoc.createElement("ATTRIBUTES")
            XMLAddedFeatID.setNodeValue(str(QId))
            XMLAddedFeatGEOM.setNodeValue(QFeat.geometry().exportToWkt ())
            self.tra.ce("XML0")
            for attr in range(0,len(QFeat.attributes())):
                self.tra.ce("ATTR:"+str(attr))
                XMLAddedFeatATTR = QDomElement()
                XMLAddedFeatATTR = XMLdoc.createElement("ATTR")
                XMLAddedFeatATTRID = QDomElement()
                XMLAddedFeatATTRID = XMLdoc.createElement("ATTRID")
                XMLAddedFeatATTRName = QDomElement()
                XMLAddedFeatATTRName.setNodeValue(str(attr))
                XMLAddedFeatATTRName = XMLdoc.createElement("ATTRNAME")
                XMLAddedFeatATTRType = QDomElement()
                XMLAddedFeatATTRType = XMLdoc.createElement("ATTRTYPE")
                XMLAddedFeatATTRValue = QDomElement()
                XMLAddedFeatATTRValue = XMLdoc.createElement("ATTRVALUE")
                XMLAddedFeatATTRValue.setNodeValue(str(QFeat.attributes()[attr]))
                self.tra.ce("XML1")
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRID)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRName)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRType)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRValue)
                XMLAddedFeatATTRS.appendChild(XMLAddedFeatATTR)
            self.tra.ce("XML2:")
            XMLAddedFeat.appendChild(XMLAddedFeatID)
            XMLAddedFeat.appendChild(XMLAddedFeatGEOM)
            XMLAddedFeat.appendChild(XMLAddedFeatATTRS)
            XMLaddedFeatures.appendChild(XMLAddedFeat)
        return XMLaddedFeatures

    def getChangedFeaturesDom(self,XMLdoc,QGeomMap):
        self.tra.ce("XMLb00")
        self.tra.ce(QGeomMap)
        XMLChangedFeatures = QDomElement()
        XMLChangedFeatures = XMLdoc.createElement("CHANGEDFEATURES")
        for QId, QGeom in QGeomMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QFeat)
            XMLChangedFeat = QDomElement()
            XMLChangedFeat = XMLdoc.createElement("FEAT")
            XMLChangedFeatID = QDomElement()
            XMLChangedFeatID = XMLdoc.createElement("ID")
            XMLChangedFeatGEOM = QDomElement()
            XMLChangedFeatGEOM = XMLdoc.createElement("GEOMETRY")
            XMLChangedFeatID.setNodeValue(str(QId))
            XMLChangedFeatGEOM.setNodeValue(QFeat.geometry().exportToWkt ())
            
            XMLChangedFeat.appendChild(XMLChangedFeatID)
            XMLChangedFeat.appendChild(XMLChangedFeatGEOM)
            XMLChangedFeatures.appendChild(XMLChangedFeat)
        return XMLChangedFeatures            

    # run method that performs all the real work
    def run(self):
        vLayer = self.iface.legendInterface().currentLayer()
        if vLayer == 0 or not vLayer.isEditable():
            return
        uncommitBuffer = vLayer.editBuffer()
        self.tra = trace()
        self.tra.ce( vLayer.name())
        self.tra.ce( vLayer.editBuffer())
        self.tra.ce( vLayer.editBuffer().addedFeatures())
        XMLDocument = QDomDocument("versioning")
        XMLvLayer = QDomElement()
        XMLvLayer = XMLDocument.createElement("layer")
        XMLvLayer.setNodeValue(vLayer.name())
        #STAGE1 - addedFeatures
        XMLvLayer.appendChild(self.getSavedFeaturesDom(XMLDocument,uncommitBuffer.addedFeatures ()))
        XMLDocument.appendChild(XMLvLayer)
        #STAGE2 - ChangedFeatures
        XMLvLayer.appendChild(self.getChangedFeaturesDom(XMLDocument,uncommitBuffer.changedFeatures ()))
        XMLDocument.appendChild(XMLvLayer)
        self.tra.ce( XMLDocument.toString(2))
        # show the dialog
        #self.dlg.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            #pass

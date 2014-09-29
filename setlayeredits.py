# -*- coding: utf-8 -*-
"""
/***************************************************************************
 layerVersion/getLayerEdits
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
#from PyQt4.QtCore import QXmlStreamReader, QFile, QIODevice
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from qgis.core import *

from xml.dom import minidom

import os.path

class trace:

    def __init__(self):
        self.trace = True
        
    def ce(self,string):
        if self.trace:
            print string

class setLayerEdits:

    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

    def setChangedFeaturesDom(self,XMLdoc,QGeomMap):
        self.tra.ce("XMLb00")
        self.tra.ce(QGeomMap)
        XMLChangedFeatures = QDomElement()
        XMLChangedFeatures = XMLdoc.createElement("CHANGEDFEATURES")
        for QId, QGeom in QGeomMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QGeom)
            XMLChangedFeat = QDomElement()
            XMLChangedFeat = XMLdoc.createElement("FEAT")
            XMLChangedFeatID = QDomElement()
            XMLChangedFeatID = XMLdoc.createElement("ID")
            XMLChangedFeatGEOM = QDomElement()
            XMLChangedFeatGEOM = XMLdoc.createElement("GEOMETRY")
            XMLChangedFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLChangedFeatGEOM.appendChild(XMLdoc.createTextNode(QGeom.exportToWkt ()))
            
            XMLChangedFeat.appendChild(XMLChangedFeatID)
            XMLChangedFeat.appendChild(XMLChangedFeatGEOM)
            XMLChangedFeatures.appendChild(XMLChangedFeat)
        return XMLChangedFeatures            


    # run method that performs all the real work
    def setEditsXMLDefinition(self,xmlFile):
        #file = QFile(xmlFile)
        #file.open(QIODevice.ReadOnly)
        #XMLdef = QXmlStreamReader(file)
        #dom = minidom()
        XMLdef = minidom.parse(xmlFile)
        print XMLdef
        #STAGE0 - layerName
        LayerNameDOM = XMLdef.getElementsByTagName('LAYERID')
        LayerID = LayerNameDOM[0].firstChild.nodeValue
        print (LayerID)
        Layer = QgsMapLayerRegistry.instance().mapLayer(LayerID)
        #vLayer = self.iface.legendInterface().currentLayer()
        #if vLayer == 0 or not vLayer.isEditable():
        #    return
        #uncommitBuffer = vLayer.editBuffer()
        #self.tra = trace()
        #self.tra.ce( vLayer.name())
        #self.tra.ce( vLayer.editBuffer())
        #self.tra.ce( vLayer.editBuffer().addedFeatures())
        #XMLDocument = QDomDocument("versioning")
        #XMLvLayer = QDomElement()
        #XMLvLayer = XMLDocument.createElement("LAYER")
        #XMLvLayerName = QDomElement()
        #XMLvLayerName = XMLDocument.createElement("LAYERNAME")
        #XMLvLayerName.appendChild(XMLdoc.createTextNode(vLayer.name()))
        #XMLvLayer.appendChild(XMLvLayerName)
        #STAGE1 - addedFeatures
        #XMLvLayer.appendChild(self.getSavedFeaturesDom(XMLDocument,uncommitBuffer.addedFeatures ()))
        #XMLDocument.appendChild(XMLvLayer)
        #STAGE2 - ChangedFeatures
        ChangedFeaturesDOM = XMLdef.getElementsByTagName('CHANGEDFEATURES')
        #self.setChangedFeaturesDom(ChangedFeaturesDOM,Layer)
        #XMLvLayer.appendChild(self.getChangedFeaturesDom(XMLDocument,uncommitBuffer.changedGeometries ()))
        #XMLDocument.appendChild(XMLvLayer)
        #STAGE3 - DeletedFeatures
        #XMLvLayer.appendChild(self.getDeletedFeaturesDom(XMLDocument,uncommitBuffer.deletedFeatureIds ()))
        #XMLDocument.appendChild(XMLvLayer)
        #self.tra.ce( XMLDocument.toString(2))
        #STAGE4 - changedAttributeValues
        #XMLvLayer.appendChild(self.getChangedAttributeValuesDom(XMLDocument,uncommitBuffer.changedAttributeValues ()))
        #XMLDocument.appendChild(XMLvLayer)
        #STAGE5 - addedAttributes
        #XMLvLayer.appendChild(self.getAddedAttributesDom(XMLDocument,uncommitBuffer.addedAttributes ()))
        #XMLDocument.appendChild(XMLvLayer)
        #STAGE6 - addedAttributes
        #XMLvLayer.appendChild(self.getDeletedAttributesDom(XMLDocument,uncommitBuffer.deletedAttributeIds ()))
        #XMLDocument.appendChild(XMLvLayer)
        #self.tra.ce( XMLDocument.toString(2))
        #return XMLdef

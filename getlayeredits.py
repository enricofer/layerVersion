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
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from qgis.core import *

import os.path

class trace:

    def __init__(self):
        self.trace = None
        
    def ce(self,string):
        if self.trace:
            print string

class getLayerEdits:

    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

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
            XMLAddedFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLAddedFeatGEOM.appendChild(XMLdoc.createTextNode(QFeat.geometry().exportToWkt ()))
            #XMLAddedFeatID.setNodeValue(str(QId))
            #XMLAddedFeatGEOM.setNodeValue(QFeat.geometry().exportToWkt ())
            self.tra.ce("XML0")
            self.tra.ce(QFeat.geometry().exportToWkt ())
            for attr in range(0,len(QFeat.attributes())):
                self.tra.ce("ATTR:"+str(attr))
                XMLAddedFeatATTR = QDomElement()
                XMLAddedFeatATTR = XMLdoc.createElement("ATTR")
                XMLAddedFeatATTRID = QDomElement()
                XMLAddedFeatATTRID = XMLdoc.createElement("ATTRID")
                XMLAddedFeatATTRID.appendChild(XMLdoc.createTextNode(str(attr)))
                XMLAddedFeatATTRName = QDomElement()
                XMLAddedFeatATTRName = XMLdoc.createElement("ATTRNAME")
                XMLAddedFeatATTRType = QDomElement()
                XMLAddedFeatATTRType = XMLdoc.createElement("ATTRTYPE")
                XMLAddedFeatATTRValue = QDomElement()
                XMLAddedFeatATTRValue = XMLdoc.createElement("ATTRVALUE")
                XMLAddedFeatATTRValue.appendChild(XMLdoc.createTextNode(str(QFeat.attributes()[attr])))
                self.tra.ce(str(QFeat.attributes()[attr]))
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


    def getDeletedFeaturesDom(self,XMLdoc,QFeats):
        self.tra.ce("XMLc00")
        self.tra.ce(QFeats)
        XMLDeletedFeatures = QDomElement()
        XMLDeletedFeatures = XMLdoc.createElement("DELETEDFEATURES")
        for QId in QFeats:
            self.tra.ce(QId)
            XMLDeletedFeat = QDomElement()
            XMLDeletedFeat = XMLdoc.createElement("FEATID")
            XMLDeletedFeat.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLDeletedFeatures.appendChild(XMLDeletedFeat)
        return XMLDeletedFeatures                        


    def getChangedAttributeValuesDom(self,XMLdoc,QFeatMap):
        self.tra.ce("XML00")
        self.tra.ce(QFeatMap)
        XMLchangedAttributeValues = QDomElement()
        XMLchangedAttributeValues = XMLdoc.createElement("CHANGEDATTRIBUTESVALUES")
        for QId, QAttrs in QFeatMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QAttrs)
            XMLchangedAttributeValuesFeat = QDomElement()
            XMLchangedAttributeValuesFeat = XMLdoc.createElement("FEAT")
            XMLchangedAttributeValuesFeatID = QDomElement()
            XMLchangedAttributeValuesFeatID = XMLdoc.createElement("ID")
            XMLchangedAttributeValuesFeatATTRS = QDomElement()
            XMLchangedAttributeValuesFeatATTRS = XMLdoc.createElement("ATTRIBUTES")
            XMLchangedAttributeValuesFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            self.tra.ce("XML0")
            for attrIdx, attrValue in QAttrs.iteritems():
                self.tra.ce("ATTR:"+str(attrIdx))
                XMLchangedAttributeValuesFeatATTR = QDomElement()
                XMLchangedAttributeValuesFeatATTR = XMLdoc.createElement("ATTR")
                XMLchangedAttributeValuesFeatATTRID = QDomElement()
                XMLchangedAttributeValuesFeatATTRID = XMLdoc.createElement("ATTRID")
                XMLchangedAttributeValuesFeatATTRID.appendChild(XMLdoc.createTextNode(str(attrIdx)))
                XMLchangedAttributeValuesFeatATTRName = QDomElement()
                XMLchangedAttributeValuesFeatATTRName = XMLdoc.createElement("ATTRNAME")
                XMLchangedAttributeValuesFeatATTRType = QDomElement()
                XMLchangedAttributeValuesFeatATTRType = XMLdoc.createElement("ATTRTYPE")
                XMLchangedAttributeValuesFeatATTRValue = QDomElement()
                XMLchangedAttributeValuesFeatATTRValue = XMLdoc.createElement("ATTRVALUE")
                XMLchangedAttributeValuesFeatATTRValue.appendChild(XMLdoc.createTextNode(str(attrValue)))
                self.tra.ce(str(attrValue))
                self.tra.ce("XML1")
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRID)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRName)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRType)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRValue)
                XMLchangedAttributeValuesFeatATTRS.appendChild(XMLchangedAttributeValuesFeatATTR)
            self.tra.ce("XML2:")
            XMLchangedAttributeValuesFeat.appendChild(XMLchangedAttributeValuesFeatID)
            XMLchangedAttributeValuesFeat.appendChild(XMLchangedAttributeValuesFeatATTRS)
            XMLchangedAttributeValues.appendChild(XMLchangedAttributeValuesFeat)
        return XMLchangedAttributeValues

    def getAddedAttributesDom(self,XMLdoc,QNewAttrs):
        XMLAddedAttributes = QDomElement()
        XMLAddedAttributes = XMLdoc.createElement("ADDEDATTRIBUTES")
        for newAttr in QNewAttrs:
            XMLAddedAttribute = QDomElement()
            XMLAddedAttribute = XMLdoc.createElement("ATTR")
            XMLAddedAttributeName = QDomElement()
            XMLAddedAttributeName = XMLdoc.createElement("NAME")
            XMLAddedAttributeName.appendChild(XMLdoc.createTextNode(newAttr.name()))
            XMLAddedAttributeType = QDomElement()
            XMLAddedAttributeType = XMLdoc.createElement("TYPE")
            XMLAddedAttributeType.appendChild(XMLdoc.createTextNode(str(newAttr.type())))
            XMLAddedAttributeTypeName = QDomElement()
            XMLAddedAttributeTypeName = XMLdoc.createElement("TYPENAME")
            XMLAddedAttributeTypeName.appendChild(XMLdoc.createTextNode(newAttr.typeName()))
            XMLAddedAttributeLength = QDomElement()
            XMLAddedAttributeLength = XMLdoc.createElement("LENGTH")
            XMLAddedAttributeLength.appendChild(XMLdoc.createTextNode(str(newAttr.length())))
            XMLAddedAttributePrecision = QDomElement()
            XMLAddedAttributePrecision = XMLdoc.createElement("PRECISION")
            XMLAddedAttributePrecision.appendChild(XMLdoc.createTextNode(str(newAttr.precision())))
            XMLAddedAttributeComment = QDomElement()
            XMLAddedAttributeComment = XMLdoc.createElement("COMMENT")
            XMLAddedAttributeComment.appendChild(XMLdoc.createTextNode(str(newAttr.comment())))
            XMLAddedAttribute.appendChild(XMLAddedAttributeName)
            XMLAddedAttribute.appendChild(XMLAddedAttributeType)
            XMLAddedAttribute.appendChild(XMLAddedAttributeTypeName)
            XMLAddedAttribute.appendChild(XMLAddedAttributeLength)
            XMLAddedAttribute.appendChild(XMLAddedAttributePrecision)
            XMLAddedAttribute.appendChild(XMLAddedAttributeComment)
            XMLAddedAttributes.appendChild(XMLAddedAttribute)
        return XMLAddedAttributes


    def getDeletedAttributesDom(self,XMLdoc,QAttrsId):
        self.tra.ce("XMLc00")
        self.tra.ce(QAttrsId)
        XMLDeletedAttributes = QDomElement()
        XMLDeletedAttributes = XMLdoc.createElement("DELETEDATTRIBUTES")
        for attrId in QAttrsId:
            XMLDeletedAttribute = QDomElement()
            XMLDeletedAttribute = XMLdoc.createElement("ATTRID")
            XMLDeletedAttribute.appendChild(XMLdoc.createTextNode(str(attrId)))
            XMLDeletedAttributes.appendChild(XMLDeletedAttribute)
        return XMLDeletedAttributes

    # run method that performs all the real work
    def getEditsXMLDefinition(self,vLayer):
        #vLayer = self.iface.legendInterface().currentLayer()
        if vLayer == 0 or not vLayer.isEditable():
            return
        uncommitBuffer = vLayer.editBuffer()
        self.tra = trace()
        self.tra.ce( vLayer.name())
        self.tra.ce( vLayer.editBuffer())
        self.tra.ce( vLayer.editBuffer().addedFeatures())
        XMLDocument = QDomDocument("versioning")
        XMLvLayer = QDomElement()
        XMLvLayer = XMLDocument.createElement("LAYER")
        XMLvLayerName = QDomElement()
        XMLvLayerName = XMLDocument.createElement("LAYERID")
        XMLvLayerName.appendChild(XMLDocument.createTextNode(vLayer.id()))
        XMLvLayer.appendChild(XMLvLayerName)
        #STAGE1 - addedFeatures
        XMLvLayer.appendChild(self.getSavedFeaturesDom(XMLDocument,uncommitBuffer.addedFeatures ()))
        XMLDocument.appendChild(XMLvLayer)
        #STAGE2 - ChangedFeatures
        XMLvLayer.appendChild(self.getChangedFeaturesDom(XMLDocument,uncommitBuffer.changedGeometries ()))
        XMLDocument.appendChild(XMLvLayer)
        self.tra.ce( XMLDocument.toString(2))
        #STAGE3 - DeletedFeatures
        XMLvLayer.appendChild(self.getDeletedFeaturesDom(XMLDocument,uncommitBuffer.deletedFeatureIds ()))
        XMLDocument.appendChild(XMLvLayer)
        self.tra.ce( XMLDocument.toString(2))
        #STAGE4 - changedAttributeValues
        XMLvLayer.appendChild(self.getChangedAttributeValuesDom(XMLDocument,uncommitBuffer.changedAttributeValues ()))
        XMLDocument.appendChild(XMLvLayer)
        self.tra.ce( XMLDocument.toString(2))
        #STAGE5 - addedAttributes
        XMLvLayer.appendChild(self.getAddedAttributesDom(XMLDocument,uncommitBuffer.addedAttributes ()))
        XMLDocument.appendChild(XMLvLayer)
        #STAGE6 - addedAttributes
        XMLvLayer.appendChild(self.getDeletedAttributesDom(XMLDocument,uncommitBuffer.deletedAttributeIds ()))
        XMLDocument.appendChild(XMLvLayer)
        self.tra.ce( XMLDocument.toString(2))
        return XMLDocument

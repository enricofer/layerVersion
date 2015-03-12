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
from datetime import datetime
from checksumlib import *

import os.path
#import checksumlib


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
        self.tra = trace()

    def getAddedFeaturesDom(self,XMLdoc,QFeatMap):
        self.tra.ce("addedFeats")
        self.tra.ce(QFeatMap)
        XMLaddedFeatures = QDomElement()
        XMLaddedFeatures = XMLdoc.createElement("ADDEDFEATURES")

        for QId, QFeat in QFeatMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QFeat)
            XMLAddedFeat = QDomElement()
            XMLAddedFeat = XMLdoc.createElement("ADDEDFEAT")
            XMLAddedFeatID = QDomElement()
            XMLAddedFeatID = XMLdoc.createElement("ID")
            XMLAddedFeatGEOM = QDomElement()
            XMLAddedFeatGEOM = XMLdoc.createElement("GEOMETRY")
            XMLAddedFeatATTRS = QDomElement()
            XMLAddedFeatATTRS = XMLdoc.createElement("ATTRIBUTES")
            XMLAddedFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLAddedFeatGEOM.appendChild(XMLdoc.createTextNode(QFeat.geometry().exportToWkt()))
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
                try:
                    XMLAddedFeatATTRValue.appendChild(XMLdoc.createTextNode(str(QFeat.attributes()[attr])))
                except:
                    XMLAddedFeatATTRValue.appendChild(XMLdoc.createTextNode(QFeat.attributes()[attr]))
                self.tra.ce(QFeat.attributes()[attr])
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRID)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRName)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRType)
                XMLAddedFeatATTR.appendChild(XMLAddedFeatATTRValue)
                XMLAddedFeatATTRS.appendChild(XMLAddedFeatATTR)
            XMLAddedFeat.appendChild(XMLAddedFeatID)
            XMLAddedFeat.appendChild(XMLAddedFeatGEOM)
            XMLAddedFeat.appendChild(XMLAddedFeatATTRS)
            XMLaddedFeatures.appendChild(XMLAddedFeat)
        return XMLaddedFeatures

    def getChangedFeaturesDom(self,XMLdoc,QGeomMap):
        self.tra.ce("changedGeoms")
        self.tra.ce(QGeomMap)
        XMLChangedFeatures = QDomElement()
        XMLChangedFeatures = XMLdoc.createElement("CHANGEDFEATURES")
        for QId, QGeom in QGeomMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QGeom)
            XMLChangedFeat = QDomElement()
            XMLChangedFeat = XMLdoc.createElement("CHANGEDFEAT")
            XMLChangedFeatID = QDomElement()
            XMLChangedFeatID = XMLdoc.createElement("ID")
            XMLChangedFeatChecksum = QDomElement()
            XMLChangedFeatChecksum = XMLdoc.createElement("CHECKSUM")
            XMLChangedFeatGEOM = QDomElement()
            XMLChangedFeatGEOM = XMLdoc.createElement("GEOMETRY")
            XMLChangedFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLChangedFeatGEOM.appendChild(XMLdoc.createTextNode(QGeom.exportToWkt ()))
            for feat in self.vLayer.getFeatures(QgsFeatureRequest(QId)):
                chk = checksumFeat(feat)
                self.tra.ce("CHECKSUM->"+chk)
                XMLChangedFeatChecksum.appendChild(XMLdoc.createTextNode(chk))
            XMLChangedFeat.appendChild(XMLChangedFeatID)
            XMLChangedFeat.appendChild(XMLChangedFeatGEOM)
            XMLChangedFeat.appendChild(XMLChangedFeatChecksum)
            XMLChangedFeatures.appendChild(XMLChangedFeat)
        return XMLChangedFeatures            


    def getDeletedFeaturesDom(self,XMLdoc,QFeats):
        self.tra.ce("deletedFeats")
        self.tra.ce(QFeats)
        XMLDeletedFeatures = QDomElement()
        XMLDeletedFeatures = XMLdoc.createElement("DELETEDFEATURES")
        for QId in QFeats:
            self.tra.ce(QId)
            XMLDeletedFeat = QDomElement()
            XMLDeletedFeat = XMLdoc.createElement("DELETEDID")
            XMLDeletedFeat.appendChild(XMLdoc.createTextNode(str(QId)))
            XMLDeletedFeatures.appendChild(XMLDeletedFeat)
        return XMLDeletedFeatures                        


    def getChangedAttributeValuesDom(self,XMLdoc,QFeatMap):
        self.tra.ce("changedAttrs")
        XMLchangedAttributeValues = QDomElement()
        XMLchangedAttributeValues = XMLdoc.createElement("CHANGEDATTRIBUTESVALUES")
        for QId, QAttrs in QFeatMap.iteritems():
            self.tra.ce(QId)
            self.tra.ce(QAttrs)
            XMLchangedAttributeValuesFeat = QDomElement()
            XMLchangedAttributeValuesFeat = XMLdoc.createElement("CHANGEDATTRIBUTESFEAT")
            XMLchangedAttributeValuesFeatID = QDomElement()
            XMLchangedAttributeValuesFeatID = XMLdoc.createElement("ID")
            XMLchangedAttributeValuesFeatCheckSum = QDomElement()
            XMLchangedAttributeValuesFeatCheckSum = XMLdoc.createElement("CHECKSUM")
            XMLchangedAttributeValuesFeatATTRS = QDomElement()
            XMLchangedAttributeValuesFeatATTRS = XMLdoc.createElement("ATTRIBUTES")
            XMLchangedAttributeValuesFeatID.appendChild(XMLdoc.createTextNode(str(QId)))
            for feat in self.vLayer.getFeatures(QgsFeatureRequest(QId)):
                XMLchangedAttributeValuesFeatCheckSum.appendChild(XMLdoc.createTextNode(checksumAttrs(feat)))
            self.tra.ce("XML0")
            for attrIdx, attrValue in QAttrs.iteritems():
                self.tra.ce("ATTR:"+str(attrIdx))
                XMLchangedAttributeValuesFeatATTR = QDomElement()
                XMLchangedAttributeValuesFeatATTR = XMLdoc.createElement("CHANGEDATTR")
                XMLchangedAttributeValuesFeatATTRID = QDomElement()
                XMLchangedAttributeValuesFeatATTRID = XMLdoc.createElement("ATTRID")
                XMLchangedAttributeValuesFeatATTRID.appendChild(XMLdoc.createTextNode(str(attrIdx)))
                XMLchangedAttributeValuesFeatATTRName = QDomElement()
                XMLchangedAttributeValuesFeatATTRName = XMLdoc.createElement("ATTRNAME")
                XMLchangedAttributeValuesFeatATTRType = QDomElement()
                XMLchangedAttributeValuesFeatATTRType = XMLdoc.createElement("ATTRTYPE")
                XMLchangedAttributeValuesFeatATTRValue = QDomElement()
                XMLchangedAttributeValuesFeatATTRValue = XMLdoc.createElement("ATTRVALUE")
                try:
                    XMLchangedAttributeValuesFeatATTRValue.appendChild(XMLdoc.createTextNode(str(attrValue)))
                except:
                    XMLchangedAttributeValuesFeatATTRValue.appendChild(XMLdoc.createTextNode(attrValue))
                self.tra.ce(attrValue)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRID)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRName)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRType)
                XMLchangedAttributeValuesFeatATTR.appendChild(XMLchangedAttributeValuesFeatATTRValue)
                XMLchangedAttributeValuesFeatATTRS.appendChild(XMLchangedAttributeValuesFeatATTR)
            XMLchangedAttributeValuesFeat.appendChild(XMLchangedAttributeValuesFeatID)
            XMLchangedAttributeValuesFeat.appendChild(XMLchangedAttributeValuesFeatATTRS)
            XMLchangedAttributeValuesFeat.appendChild(XMLchangedAttributeValuesFeatCheckSum)
            XMLchangedAttributeValues.appendChild(XMLchangedAttributeValuesFeat)
        return XMLchangedAttributeValues

    def getAddedAttributesDom(self,XMLdoc,QNewAttrs):
        XMLAddedAttributes = QDomElement()
        XMLAddedAttributes = XMLdoc.createElement("ADDEDATTRIBUTES")
        XMLAddedAttributesCheckSum = QDomElement()
        XMLAddedAttributesCheckSum = XMLdoc.createElement("CHECKSUM")
        XMLAddedAttributesCheckSum.appendChild(XMLdoc.createTextNode(checksumLayerDef(self.vLayer)))
        XMLAddedAttributes.appendChild(XMLAddedAttributesCheckSum)
        for newAttr in QNewAttrs:
            XMLAddedAttribute = QDomElement()
            XMLAddedAttribute = XMLdoc.createElement("ADDEDATTR")
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
    def getEditsXMLDefinition(self):
        XMLDocument = QDomDocument("QGISlayersEditsVersioning")
        self.tra.ce( self.iface.editableLayers())
        XMLVersion = QDomElement()
        XMLVersion = XMLDocument.createElement("QGISlayersEditsVersioning")
        XMLVersionDate = QDomElement()
        XMLVersionDate = XMLDocument.createElement("VERSIONDATE")
        XMLVersionDate.appendChild(XMLDocument.createTextNode(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        XMLVersion.appendChild(XMLVersionDate)
        for self.vLayer in self.iface.editableLayers():
        #vLayer = self.iface.legendInterface().currentLayer()
        #if vLayer == 0 or not vLayer.isEditable():
        #    return
            self.uncommitBuffer = self.vLayer.editBuffer()
            self.tra.ce( "CHECKSUM")
            self.tra.ce( self.vLayer.name())
            self.tra.ce( checksum(self.vLayer))
            XMLvLayer = QDomElement()
            XMLvLayer = XMLDocument.createElement("LAYER")
            XMLvLayerID = QDomElement()
            XMLvLayerID = XMLDocument.createElement("LAYERID")
            XMLvLayerID.appendChild(XMLDocument.createTextNode(self.vLayer.id()))
            XMLvLayer.appendChild(XMLvLayerID)
            XMLvLayerName = QDomElement()
            XMLvLayerName = XMLDocument.createElement("LAYERNAME")
            XMLvLayerName.appendChild(XMLDocument.createTextNode(self.vLayer.name()))
            XMLvLayer.appendChild(XMLvLayerName)
            XMLvLayerCheckusum = QDomElement()
            XMLvLayerCheckusum = XMLDocument.createElement("LAYERCHECKSUM")
            XMLvLayerCheckusum.appendChild(XMLDocument.createTextNode(checksum(self.vLayer)))
            XMLvLayer.appendChild(XMLvLayerCheckusum)
            #STAGE1 - addedFeatures
            XMLvLayer.appendChild(self.getAddedFeaturesDom(XMLDocument,self.uncommitBuffer.addedFeatures ()))
            XMLVersion.appendChild(XMLvLayer)
            #STAGE2 - ChangedFeatures
            XMLvLayer.appendChild(self.getChangedFeaturesDom(XMLDocument,self.uncommitBuffer.changedGeometries ()))
            XMLVersion.appendChild(XMLvLayer)
            self.tra.ce( XMLDocument.toString(2))
            #STAGE3 - DeletedFeatures
            XMLvLayer.appendChild(self.getDeletedFeaturesDom(XMLDocument,self.uncommitBuffer.deletedFeatureIds ()))
            XMLVersion.appendChild(XMLvLayer)
            self.tra.ce( XMLDocument.toString(2))
            #STAGE4 - changedAttributeValues
            XMLvLayer.appendChild(self.getChangedAttributeValuesDom(XMLDocument,self.uncommitBuffer.changedAttributeValues ()))
            XMLVersion.appendChild(XMLvLayer)
            self.tra.ce( XMLDocument.toString(2))
            #STAGE5 - addedAttributes
            XMLvLayer.appendChild(self.getAddedAttributesDom(XMLDocument,self.uncommitBuffer.addedAttributes ()))
            XMLVersion.appendChild(XMLvLayer)
            #STAGE6 - addedAttributes
            XMLvLayer.appendChild(self.getDeletedAttributesDom(XMLDocument,self.uncommitBuffer.deletedAttributeIds ()))
            XMLVersion.appendChild(XMLvLayer)
        #self.tra.ce( XMLDocument.toString(2))
        XMLDocument.appendChild(XMLVersion)
        return XMLDocument

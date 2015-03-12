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
from qgis.core import *
from qgis.gui import *
from datetime import datetime
from checksumlib import *

from xml.dom import minidom

import os.path

class trace:

    def __init__(self):
        self.trace = True
        
    def ce(self,string):
        if self.trace:
            print string


class setLayerEdits:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.tra = trace()
        self.trac = trace()
        self.trac.trace = True
        colorSource = QColor(250,0,0,200)
        self.targetEvid = QgsRubberBand(self.iface.mapCanvas(), QGis.Line)
        self.targetEvid.setColor(colorSource)
        self.targetEvid.setWidth(3)


    def getTypeFieldsList(self, layer):
        alist=[]
        fieldsDef = layer.pendingFields()
        for field in fieldsDef:
            newValue = QVariant()
            alist.append(newValue)
        return alist

    def getTypeFieldsDef(self,layer):
        typeFields = []
        fieldsDef = layer.pendingFields()
        for field in fieldsDef:
            typeFields.append(str(field.typeName().lower()))
        return typeFields

    def setAddedFeaturesDom(self, DOM, Layer):
        #addedFeaturesDOM = DOM.getElementsByTagName('ADDEDFEATURES')
        #testDOM = QDomDocument("test")
        featsDOM = DOM.getElementsByTagName('ADDEDFEAT')
        Layer.editBuffer().featureAdded.connect(self.checkFeat)
        if not featsDOM:
            return
        feats = []
        idAddedFeat = -10000
        for featDOM in featsDOM:
            featIDDOM = featDOM.getElementsByTagName('ID')
            featID = int(featIDDOM[0].firstChild.nodeValue)
            featGEOMDOM = featDOM.getElementsByTagName('GEOMETRY')
            featGEOM = featGEOMDOM[0].firstChild.nodeValue
            #featATTRSDOM = featDOM.getElementsByTagName('ATTRIBUTES')
            attrsDOM = featDOM.getElementsByTagName('ATTR')
            QAttrs = []
            typeFieldsDef = self.getTypeFieldsDef(Layer)
            self.tra.ce("ADDEDFEAT "+Layer.name())
            self.tra.ce(attrsDOM)
            self.tra.ce(typeFieldsDef)
            #idx = 0
            addFeat = QgsFeature()
            addGeom = QgsGeometry().fromWkt(featGEOM.encode('ascii', 'ignore'))
            addFeat.setGeometry(QgsGeometry(addGeom))

            for attrDOM in attrsDOM:
                attrIDDOM = attrDOM.getElementsByTagName('ATTRID')
                attrID = int(attrIDDOM[0].firstChild.nodeValue)
                attrValueDOM = attrDOM.getElementsByTagName('ATTRVALUE')
                if attrValueDOM[0].hasChildNodes():
                    attrRawValue= attrValueDOM[0].firstChild.nodeValue
                else:
                    attrRawValue = None
                self.tra.ce(attrID)
                self.tra.ce(attrRawValue)
                QAttrs.append(attrRawValue)
                '''
                try:
                    addFeat.setAttribute(attrID,float(attrRawValue))
                except:
                    try:
                        addFeat.setAttribute(attrID,int(attrRawValue))
                    except:
                        addFeat.setAttribute(attrID,attrRawValue)

                if attrRawValue != 'NULL':
                    if typeFieldsDef[attrID] == 'string':
                        QAttrs.append(attrRawValue)
                    elif typeFieldsDef[attrID] == 'real':
                        QAttrs.append(float(attrRawValue))
                    elif typeFieldsDef[attrID] == 'integer':
                        QAttrs.append(int(attrRawValue))
                else:
                	QAttrs.append(None)
                '''

            addFeat.setAttributes(QAttrs)
            feats.append(addFeat)
            idAddedFeat -= 1

        Layer.editBuffer().addFeatures(feats)
        Layer.triggerRepaint()
        self.iface.mapCanvas().refresh()
            
    def checkFeat(self, id):
        self.trac.ce("FEATURE OP")
        self.trac.ce(id)

    def setChangedFeaturesDom(self,DOM,Layer):
        #changedFeaturesDOM = DOM.getElementsByTagName('CHANGEDFEATURES')
        featsDOM = DOM.getElementsByTagName('CHANGEDFEAT')
        for featDOM in featsDOM:
            featIDDOM = featDOM.getElementsByTagName('ID')
            featID = int(featIDDOM[0].firstChild.nodeValue)
            featCheckDOM = featDOM.getElementsByTagName('CHECKSUM')
            if featCheckDOM[0].hasChildNodes():
                featCheck = featCheckDOM[0].firstChild.nodeValue
            else:
                featCheck = None
            featIDDOM = featDOM.getElementsByTagName('GEOMETRY')
            featGEOM = featIDDOM[0].firstChild.nodeValue
            targetFeats = Layer.getFeatures(QgsFeatureRequest(featID))
            self.trac.ce(featID)
            self.trac.ce(targetFeats)
            for feat in targetFeats:
                self.trac.ce(feat)
                targetFeat = feat
            geom = QgsGeometry().fromWkt(featGEOM)
            self.trac.ce(featCheck)
            self.trac.ce(checksumFeat(targetFeat))
            reply = QMessageBox.Yes
            #print checksumFeat(targetFeat), featCheck
            if featCheck and checksumFeat(targetFeat) != featCheck:
                self.targetEvid.setToGeometry(geom,Layer)
                featureBox = geom.boundingBox()
                self.iface.mapCanvas().setExtent(featureBox)
                self.iface.mapCanvas().refresh()
                reply = QMessageBox.question(None,"Geometry changed","The Highlighted geometry appears to be changed before edit restore.\nDo you want to cancel restored geometry changes and keep exing feature?", QMessageBox.Yes, QMessageBox.No)
                self.targetEvid.reset()
            if reply == QMessageBox.Yes:
                Layer.changeGeometry(featID, geom)
                
    def setDeletedFeaturesDom(self,DOM,Layer):
        self.tra.ce("DELETING FROM LAYER "+Layer.name())
        deletedFeatsDOM = DOM.getElementsByTagName('DELETEDID')
        self.tra.ce("ELEMENT HAS "+str(deletedFeatsDOM.length)+" CHILDNODES")
        if deletedFeatsDOM.length == 0:
            return
        for deletedDOM in deletedFeatsDOM:
            featID = int(deletedDOM.firstChild.nodeValue)
            self.tra.ce(str(featID)+'ok')
            Layer.deleteFeature(featID)

    def setChangedAttributesValuesDom(self,DOM,Layer):
        typeFieldsDef = self.getTypeFieldsDef(Layer)
        self.tra.ce(typeFieldsDef)
        self.tra.ce('CHANGEDATTRIBUTES')
        featsDOM = DOM.getElementsByTagName('CHANGEDATTRIBUTESFEAT')
        for featDOM in featsDOM:
            featIDDOM = featDOM.getElementsByTagName('ID')
            featID = int(featIDDOM[0].firstChild.nodeValue)
            attrsDOM = featDOM.getElementsByTagName('CHANGEDATTR')
            self.tra.ce(featID)
            features = Layer.getFeatures(QgsFeatureRequest(featID))
            for feature in features:
                for attrDOM in attrsDOM:
                    attrIDDOM = attrDOM.getElementsByTagName('ATTRID')
                    attrID = int(attrIDDOM[0].firstChild.nodeValue)
                    attrValueDOM = attrDOM.getElementsByTagName('ATTRVALUE')
                    attrRawValue= attrValueDOM[0].firstChild.nodeValue
                    self.tra.ce("ATTRID:"+str(attrID)+" ATTRRAW:"+attrRawValue+" ATTRTYPE:"+typeFieldsDef[attrID])
                    self.tra.ce(typeFieldsDef)
                    feature.setAttribute(attrID,attrRawValue)
                    '''
                    if typeFieldsDef[attrID] == 'string':
                        try:
                            #Layer.changeAttributeValue(featID, attrID, attrRawValue)
                            #feature[attrID]=attrRawValue
                            feature.setAttribute(attrID,attrRawValue)
                        except:
                            Layer.changeAttributeValue(featID, attrID, None)
                        self.tra.ce('string')
                    elif typeFieldsDef[attrID] == 'real':
                        try
                            #Layer.changeAttributeValue(featID, attrID, float(attrRawValue))
                            #feature[attrID]=float(attrRawValue)
                            feature.setAttribute(attrID,float(attrRawValue))
                        except:
                            Layer.changeAttributeValue(featID, attrID, None)
                        self.tra.ce('real')
                    elif typeFieldsDef[attrID] == 'integer':
                        try:
                            #Layer.changeAttributeValue(featID, attrID, int(attrRawValue))
                            feature.setAttribute(attrID,int(attrRawValue))
                            #feature['new1']=int(attrRawValue)
                        except:
                            Layer.changeAttributeValue(featID, attrID, None)
                        self.tra.ce('integer')
                    '''
                    Layer.updateFeature(feature)
                    self.tra.ce(feature.attributes())

    def setAddedAttributesDom(self,DOM,Layer):
        typeFieldsDef = self.getTypeFieldsDef(Layer)
        self.tra.ce('setAddedAttributesDom-begin')
        addedAttrsDOM = DOM.getElementsByTagName('ADDEDATTR')
        for addedAttrDOM in addedAttrsDOM:
           addedAttrNameDOM = addedAttrDOM.getElementsByTagName('NAME')
           addedAttrName = addedAttrNameDOM[0].firstChild.nodeValue
           addedAttrTypeDOM = addedAttrDOM.getElementsByTagName('TYPE')
           addedAttrType = int(addedAttrTypeDOM[0].firstChild.nodeValue)
           addedAttrTypeNameDOM = addedAttrDOM.getElementsByTagName('TYPENAME')
           addedAttrTypeName = addedAttrTypeNameDOM[0].firstChild.nodeValue
           addedAttrLengthDOM = addedAttrDOM.getElementsByTagName('LENGTH')
           addedAttrLength = int(addedAttrLengthDOM[0].firstChild.nodeValue)
           addedAttrPrecisionDOM = addedAttrDOM.getElementsByTagName('PRECISION')
           addedAttrPrecision = int(addedAttrPrecisionDOM[0].firstChild.nodeValue)
           addedAttrCommentDOM = addedAttrDOM.getElementsByTagName('COMMENT')
           if addedAttrCommentDOM[0].firstChild:
               addedAttrComment = addedAttrCommentDOM[0].firstChild.nodeValue
           else:
               addedAttrComment = ""
           Layer.addAttribute(QgsField(addedAttrName,addedAttrType,addedAttrTypeName,addedAttrLength,addedAttrPrecision,addedAttrComment))
           #Layer.addAttribute(QgsField(addedAttrName,QVariant.Int))
           fieldsString = ""
           for f in Layer.pendingFields():
              fieldsString += f.name()+", "
           self.tra.ce(fieldsString)
        Layer.updateFields()
        self.tra.ce('setAddedAttributesDom-end')

    def setDeletedAttributesDom(self,DOM,Layer):
        self.tra.ce('setDeletedAttributesDom-end')
        attrsDOM = DOM.getElementsByTagName('DELETEDATTRIBUTES')
        for attrDOM in attrsDOM:
            attrIDDOM = attrDOM.getElementsByTagName('ATTRID')
            if attrIDDOM:
                attrID = int(attrIDDOM[0].firstChild.nodeValue)
                Layer.dataProvider().deleteAttributes( [ attrID ] )
        Layer.updateFields()
        self.tra.ce('setDeletedAttributesDom-end')

    # run method that performs all the real work
    def setEditsXMLDefinition(self,xmlFile):
        #file = QFile(xmlFile)
        #file.open(QIODevice.ReadOnly)
        #XMLdef = QXmlStreamReader(file)
        #dom = minidom()
        self.tra.ce(xmlFile)
        XMLdef = minidom.parse(xmlFile)
        VersionDateDOM = XMLdef.getElementsByTagName('VERSIONDATE')
        VersionDate = datetime.strptime(VersionDateDOM[0].firstChild.nodeValue,'%Y-%m-%d %H:%M:%S')
        LayersDOM = XMLdef.getElementsByTagName('LAYER')
        LayersDef=[]
        LayersNames=""
        LayersChanged=""
        LayersMissed=""
        for LayerDOM in LayersDOM:
            if LayerDOM:
                #STAGE0 - layerName and checksum
                LayerIDDOM = LayerDOM.getElementsByTagName('LAYERID')
                LayerID = LayerIDDOM[0].firstChild.nodeValue
                LayerNameDOM = LayerDOM.getElementsByTagName('LAYERNAME')
                LayerName = LayerNameDOM[0].firstChild.nodeValue
                LayerVersionChecksumDOM = LayerDOM.getElementsByTagName('LAYERCHECKSUM')
                LayerVersionChecksum = LayerVersionChecksumDOM[0].firstChild.nodeValue
                L = QgsMapLayerRegistry.instance().mapLayer(LayerID)
                LayersDef.append({'DOM':LayerDOM,'layer':L})
                LayersNames += LayerName+"\n"
                try:
                    check = checksum(L)
                except:
                    check = ""
                self.tra.ce(LayerName+" "+check)
                if not LayerID in QgsMapLayerRegistry.instance().mapLayers():
                    LayersMissed += LayerName+"\n"
                if check != LayerVersionChecksum:
                    LayersChanged += LayerName+"\n"
        oldTime = datetime.now()-VersionDate
        if oldTime.days > 0:
            oldTimeString = str(oldTime.days) + ' days'
        elif oldTime.seconds > 3600:
            oldTimeString = str(int(oldTime.seconds/3600)) + ' hours'
        else:
            oldTimeString = str(int(oldTime.seconds/60)) + ' minutes'
        quit_msg = 'You are about to import a version file that is %s old and affects the following layers:\n%s' % (oldTimeString,LayersNames)
        
        if LayersMissed != "":
            QMessageBox.critical(None, "Version Layers missed", "Can't restore version. Following layer are missed:\n"+LayersMissed)
            return
        if LayersChanged != "":
            quit_msg = quit_msg + "\nand the following layers appears to be changed from version save:\n"+ LayersChanged + "\nReconcile is needed."
            alert_msg = "Importing layers edits version: LAYER CHANGED!"
        else:
            alert_msg = "Importing layers edits version"
        quit_msg = quit_msg + "\nDo you want to edit layers to import version data?"
        reply = QMessageBox.question(None,alert_msg,quit_msg, QMessageBox.Yes, QMessageBox.No)
        self.tra.ce(LayersDef)
        if reply == QMessageBox.Yes: 
            for LayerDef in LayersDef:
                LayerDef['layer'].startEditing ()
                #STAGE1 - deletedAttributes 
                self.setAddedAttributesDom(LayerDef['DOM'],LayerDef['layer'])
                #STAGE2 - addedAttributes
                self.setDeletedAttributesDom(LayerDef['DOM'],LayerDef['layer'])
                #STAGE3 - addedFeatures
                self.setAddedFeaturesDom(LayerDef['DOM'],LayerDef['layer'])
                #STAGE4 - ChangedFeatures
                self.setChangedFeaturesDom(LayerDef['DOM'],LayerDef['layer'])
                #STAGE5 - DeletedFeatures
                self.setDeletedFeaturesDom(LayerDef['DOM'],LayerDef['layer'])
                #STAGE6 - changedAttributeValues
                self.setChangedAttributesValuesDom(LayerDef['DOM'],LayerDef['layer'])
            self.iface.mapCanvas().refresh()

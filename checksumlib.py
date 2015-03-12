# -*- coding: utf-8 -*-
"""
/***************************************************************************
 layerVersion/checksumlib
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
import hashlib


# procedure by  Joshua Arnott: http://snorf.net/blog/2014/01/04/writing-unit-tests-for-qgis-python-plugins/
def checksum(layer):
    m = hashlib.md5()
    m.update(layer.crs().toProj4())
    field_names = [f.name() for f in layer.dataProvider().fields().toList()].__repr__()
    m.update(field_names)
    features = layer.dataProvider().getFeatures()
    for feature in features:
        try:
            m.update(feature.geometry().exportToWkt())
            m.update(feature.attributes().__repr__())
        except:
            pass
    return m.hexdigest()

def checksumLayerDef(layer):
    m = hashlib.md5()
    m.update(layer.crs().toProj4())
    field_names = [f.name() for f in layer.dataProvider().fields().toList()].__repr__()
    m.update(field_names)
    return m.hexdigest()

def checksumFeat(feature):
    m = hashlib.md5()
    field_names = [f.name() for f in feature.fields().toList()].__repr__()
    m.update(field_names)
    try:
        m.update(feature.geometry().exporttowkt())
        m.update(feature.attributes().__repr__())
    except:
        pass
    return m.hexdigest()

def checksumAttrs(feature):
    m = hashlib.md5()
    field_names = [f.name() for f in feature.fields().toList()].__repr__()
    m.update(field_names)
    try:
        m.update(feature.attributes().__repr__())
    except:
        pass
    return m.hexdigest()

def checksumGeom(feature):
    m = hashlib.md5()
    field_names = [f.name() for f in feature.fields().toList()].__repr__()
    m.update(field_names)
    try:
        m.update(feature.geometry().exporttowkt())
    except:
        pass
    return m.hexdigest()
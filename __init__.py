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
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load layerVersion class from file layerVersion
    from layerversion import layerVersion
    return layerVersion(iface)

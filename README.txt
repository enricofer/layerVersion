I am architect and urban planner and I like to made tools for my everyday work. One of my tasks is to keep up to date the urban planning act whose variations must be discussed, revised and approved before they become law. The common way to do this is working in a spatial database environment with “versioning” capability. A “version” is a snapshot of the spatial database where all the transactions that bring to the final variation are tracked and stored before definitive commit.

There are not many way to do this. Oracle Spatial and ArcSDE have powerful versioning tools but they can not be used in a QGis environment. Working in Qgis we can use the PostGis tables versioning function added to core DbManager plugin, that appears to be very powerful but it is poorly documented. Anyway there would be no alternative to geodatabase, but not always we would be interested to deal with it. The tool I need has to be more flexible and does allow using many datasources and expecially must be ready to use without the need of organizing complex data structures.

The answer came digging the Qgis Api Documentation. In QgsVectorLayerEditBuffer class I found all the method to handle current edits before they were committed to datasource so I said: Why not to save them in a separate file that can be restored to replicate edits everytime and everywhere there are the same layers? The layerVersion plugin has a quite simple implementation. It get edits from every current edited layer:

1) the newly added features from addedFeatures() method;

2) the features that has attributes table edits from changedAttributeValues() method;

3) the erased attributes from deletedAttributeIds()method;

4) the new attributes from addedAttributes()method;

5) the features that have changed the geometry from changedGeometries() method;

6) and finally the deleted features from deletedFeatureIds() method;

then stores everything in a xml file along with some crc checksums to validate data. All the edits saved in the “.qlv” file can be restored reproducing all the modification stored, doing some checks to ensure data consistency in the case the layers were modified. That’s all. The “.qlv” version file can be restored in every qgis project with the same loaded layers, so can be shared with other users to complete edits for their responsible area or to deliver partial modificazioni of great geodatabases.

The first release of the plugin is flagged as experimental because possible bugs can cause data losses and should be be used with caution, verifying the succesful restoration of versions. In this regard, I would ask to all interested users to report issues as soon as possible to github issue tracking page.

The plugin has a very minimal user interface: it adds an item under vector menu and adds two buttons to Qgis interface: save and load layer versions.
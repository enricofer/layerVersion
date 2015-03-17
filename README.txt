I am a architect and urban planner in a and I love to made tools for my everyday work. One of my task is to keep up to date the urban planning act whose variations must be discussed and approved.
The common way to do this is working in a spatial database environment with "versioning" capability. A "version" is a snapshot of the spatial database where all the transactions that bring to the final variation are tracked and stored before definitive commit.
There are not many way to do this. Oracle Spatial and ArcSDE have powerful versioning tools but they can not be used in a QGis environment. Working in Qgis all we can do is to use the PostGis tables versioning function added to core DbManager plugin, that appears to be very powerful but very poorly documented. Anyway there would be appear no alternative to geodatabase.
The tool I need has to be more flexible and does allow using many datasources and expecially must be ready to use without complex data structures organization.
The answer came digging the Qgis Api Documentation. In QgsVectorLayerEditBuffer class (http://qgis.org/api/2.8/classQgsVectorLayerEditBuffer.html) I found all the method to handle current edits before they are committed to datasource so I tell to me: Why not save them in a separate file that can be restored to replicate edits everytime and everywhere there are the same layers?
The layerVersion plugin has a quite simple implementation. It get edits from every current edited layer:
1)the newly added features from addedFeatures() method
2)the features that has attributes table edits from changedAttributeValues() method
3)the erased attributes from deletedAttributeIds()method
4)the new attributes from addedAttributes()method
5)the features that have changed the geometry from changedGeometries() method
6)and finally the deletede features from deletedFeatureIds() method
and stores everything in a xml file along with some crc checksums to validate data. All the edits saved in the ".qlv" file can be restored reproducing all the modification stored. That's all. The ".qlv" version file can be restored in every qgis project where can be found the same layers, so can be shared with other users to complete edits for their responsible area or to deliver partial modifications of great geodatabases.
The first release of the plugin is flagged as experimental because possible bugs can bring to data losses. I ask to all interested users to report issues as soon as possible to github issue tracking page.
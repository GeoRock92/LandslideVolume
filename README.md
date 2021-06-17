# LandslideVolume

This is a short python script to calculate volume of landslides when using ArcGIS.

**Requirements**
Spatial Analyst extension
A good dataset to have fun with

**Rationale**

There is no built-in function (or at least, there was not some time ago) to calculate volumes of landslides efficiently, but instead, the procedure was rather tedious. It requires clicking in several tools and checking that everything is correct. This is a problem when several landslides are to be analysed. And anyone who has worked with data knows that this is an excellent way to introduce mistakes.

The script requires to map the contour of a landslide by using a polygon, which creates a shapefile (e.g. 'shapefile1'). The scrip then utilises 'shapefile1' to perform a series of slope reconstructions and TINs to finally calculate the volumetric difference between the reconstructed "initial" slope and the current "slided" slope.

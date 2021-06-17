import arcpy
from arcpy import env
#This is a straightforward code which is used in the python console of ArcMAP
#Javier López-Cabrera, 2016
#Environment -> Change your database
env.workspace = "C:/Path"

#Variables to change
Landslide = "Landsile_to_map" #Your shapefile identifying the landslide 
Base = "utm_topography" #This is the base topography. Please change accordingly
ReferencePlane = "Ref_Plane" #Add a reference plane so the script does not reconstruct the whole topography (which can be a huge dataset!!)

#This that shouln't touch
Interpolated = "Landsile_to_map_i"
Contour = "CLandsile_to_mapC"
TIN = "Landsile_to_map_tin"
InterpolatedFromTin = "Landsile_to_map_it"
ContourErased = "CLandsile_to_map_e"
ContourErasedTin = "CLandsile_to_map_et"
TINInterpolatedErased = "Landsile_to_map_ite"
Volume = "Landsile_to_map_volume" #This is what we are looking for, the slided volume


#From now, do not change anything - Set new environment extent landslide original
#arcpy.env.extent = Landslide

#Interpotale shape from original
#arcpy.InterpolateShape_3d(Base,Landslide,Interpolated,"#","1","BILINEAR","DENSIFY","0")

#generate fields Area, Centroids and ZMaxMin
arcpy.AddField_management(Interpolated,"Area","Double")
arcpy.AddField_management(Interpolated,"Long","Double") #Longitue and latitude coordinates of the centroid
arcpy.AddField_management(Interpolated,"Lat","Double")
arcpy.AddField_management(Interpolated,"Max_depth","Double") #Max depth of slide (or minimum height if subaerial)
arcpy.AddField_management(Interpolated,"Min_depth","Double") #Min depth of slide (or max height if subaerial)


#calculate fields
arcpy.CalculateField_management(Interpolated,"Area","!shape.area@squarekilometers!","PYTHON_9.3")
arcpy.CalculateField_management(Interpolated,"Long","!shape.extent.XMax!","PYTHON_9.3")
arcpy.CalculateField_management(Interpolated,"Lat","!shape.extent.YMax!","PYTHON_9.3")
arcpy.CalculateField_management(Interpolated,"Max_depth","!shape.extent.ZMin!","PYTHON_9.3")
arcpy.CalculateField_management(Interpolated,"Max_depth","!shape.extent.ZMax!","PYTHON_9.3")

#Set new environment extent
arcpy.env.extent = ReferencePlane

#Create contour lines
arcpy.gp.Contour_sa(Base,Contour,"10","0","1")

#Set no environment extent
arcpy.env.extent = ""

#Create tin
arcpy.CreateTin_3d(TIN,"#",Contour,"DELAUNAY")

#Interpolate shape from tin
arcpy.InterpolateShape_3d(TIN,Interpolated,InterpolatedFromTin,"#","1","LINEAR","DENSIFY","0")

#Erase contour
arcpy.Erase_analysis(Contour,Interpolated,ContourErased,"#")

#Interpolate shape contour and tin
arcpy.InterpolateShape_3d(TIN,ContourErased,ContourErasedTin,"#","1","LINEAR","DENSIFY","0")

#Create interpolated tin
arcpy.CreateTin_3d(TINInterpolatedErased,"#",ContourErasedTin,"DELAUNAY")

#Set new environment extent original
#arcpy.env.extent = Landslide

#Calculate volume
arcpy.SurfaceDifference_3d(TINInterpolatedErased,TIN,Volume,"0","0","#","10","#","#")

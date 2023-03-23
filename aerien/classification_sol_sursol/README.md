# Objective
Classify the 2020 LiDAR dataset into ground and non-ground.

# General presentation
### Tool
PDAL 2.4.1.
### Datas
The dataset covers the all SCoT (administrative subdivision for urban management) of Lille Metropole. Its density is about 100pts/km².
Transmitted as flightlines in las format, it has been compressed in squarred tiles of 500m with a 20m buffer in laz format 1.4 dataformat 8.

# Methodology
#### Choises
The datas unproceesed are
- low and highnoise classified as Low Point class 7
- ReturnNumber and NumberOf Returns < 1 as Low Point class 7
- ScanAngleRank < -8.5° and > 8.5° as Never Classified class 0

#### Processing chain
- Creating a dimension Classification with filters.ferry
- Assign all points as Unclassified class 1 with filters.assign
- Assign ReturnNumber and NumberOf Returns < 1 to class 7 and ScanAngleRank < -8.5° and > 8.5° to class 0 with filters.assign
- Classify Low Points as noise with filters.elm
- Classify Outliers as Noise with filters.outlier
- Reclassify as valids points with a OptimalRadius > 1 with filters.optimalneighborhood and then filters.assign
- Finally, classify ground and non-ground points with filters.csf
import geopandas as gpd
import shapely.wkt

import math
import time
import os.path
from datetime import datetime, date

df = gpd.read_file('D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\SpatialData\\California_Fire_Perimeters_(all).geojson')
# print(dfAll.head())

#df = gpd.read_file('D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\SpatialData\\California_Fire_Perimeters_large.geojson')

print(type(df))

headers = df.columns.to_numpy()
print(headers)

#print('printing HEAD')
#print(df.head())

columnHeaders = ['OBJECTID' 'YEAR_' 'STATE' 'AGENCY' 'UNIT_ID' 'FIRE_NAME' 'INC_NUM'
 'ALARM_DATE' 'CONT_DATE' 'CAUSE' 'COMMENTS' 'REPORT_AC' 'GIS_ACRES'
 'C_METHOD' 'OBJECTIVE' 'FIRE_NUM' 'Shape__Area' 'Shape__Length'
 'geometry']

#2020-08-16 00:00:00+00:00
#2020-09-24 00:00:00+00:00
print(df['ALARM_DATE'][0])
print(df['CONT_DATE'][0])
print(df['FIRE_NAME'][0])
print(df['geometry'][0])

#determine size for iterations

size = len(df['ALARM_DATE'])

alarm = df['ALARM_DATE'][0]
containment = df['CONT_DATE'][0]

location = df['geometry'][0]

shapes = [location.wkt]

#fire_data = []

lastValidDate = df['ALARM_DATE'][0]

output_path = 'D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\SpatialData\\SpatialDataExported.csv'
file_out = open(output_path, 'w')
file_out.write(f'startDate,endDate,latitude,longitude,acres' + '\n')
for i in range(size):
    alarm = df['ALARM_DATE'][i]
    try:
        if(len(alarm) < 10):
            alarm = lastValidDate    
        else:
            lastValidDate = alarm
    except(TypeError):
        alarm = lastValidDate  
    containment = df['CONT_DATE'][i]
    location = df['geometry'][i]
    acres = df['GIS_ACRES'][i]
    index = 0
    for shape in shapes:
        shapelyObject = shapely.wkt.loads(shape)
        for polygon in shapelyObject:
            coords = list(polygon.exterior.coords)
            #print(coords)
            for pair in coords:
                #longitude first
                #latitude second
                file_out.write(f'{alarm},{containment},{pair[1]},{pair[0]},{acres}' + '\n')
                index = index + 1
file_out.close()



# center = location.centroid.bounds

# print(center[0])
# print(center[1])
# print()

test = 0
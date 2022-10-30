import pandas as pd
import numpy as np
from source_code.data_generation import data_generation as gen
from datetime import datetime

#File Naming conventions
# weatherData naming convention YYYYdaily{StationID}
# StationID = ###

#DAILY Default Order of Data Columns:
#  A   1.  	Station Id
#  B   2. 	Date
#  C   3. 	Julian Date
#  D   4.  	Reference ETo   (in)   (mm)       
#  F   6.  	Precipitation   (in)   (mm)      
#  H   8.  	Solar Radiation Average   (Ly/day)   (W/m²)
#  J   10. 	Average Vapor Pressure   (mBars)   (kPa)
#  L   12. 	Maximum Air Temperature   (°F)   (°C)
#  N   14. 	Minimum Air Temperature   (°F)   (°C)
#  P   16. 	Average Air Temperature   (°F)   (°C)
#  R   18. 	Maximum Relative Humidity   (%)
#  T   20. 	Minimum Relative Humidity   (%)
#  V   22. 	Average Relative Humidity   (%)
#  X   24. 	Dew Point   (°F)   (°C)
#  Z   26. 	Average Wind Speed   (mph)   (m/s)
#  AB  28. 	Wind Run   (miles)   (km)
#  AD  30. 	Average Soil Temperature   (°F)   (°C)

Indices = [0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29]
ColumnNames = ['StationId','Date','JulianDate','Eto','Precipitation','SolarRadiation','VaporPressure','MaxAirTemp','MinAirTemp','AvgAirTemp',
                'MaxRelHumidity','MinRelHumidity', 'AvgRelHumidity', 'DewPoint', 'AvgWindSpeed', 'AvgSoilTemp']

Latitudes = [36.814000,36.336222,36.881000,36.972000,35.532695,38.535794,36.851248,40.044065,35.238000,35.077222,35.160000,
39.608639,38.752307,39.739000,36.158138,36.905000,32.846000,33.077000,36.768256,36.040000,35.867750,36.490000,36.174000,
33.631000,33.764000,35.505000,38.808000,36.447000,36.516000,38.870600,35.703000,39.226861,36.301000,33.489000,37.358606,
33.655000,36.620000,34.954000,36.597481,36.683000,33.043151,38.109000,41.063767,33.964942,32.787000,41.792000,37.928154,
42.003000,33.256000,33.646000,38.662000,35.305442,36.341000,35.649861,33.730000,37.097450,40.289799,34.302000,35.114000,
34.903000,39.691782,33.486650,38.121000,34.583144,37.914000,32.733000,34.432000,32.759575,37.326000,37.834822,37.645222,
33.388000,34.147000,33.090000,33.688450,34.924000,38.428475,34.056589,38.549000,36.820833,38.523000,34.130000,38.403550,
39.252561,39.006747,36.360647,32.806183,34.942525,36.609444,41.438214,41.958869,37.231861,35.286000,34.471579,36.886000,
37.453000,34.173000,33.049000,34.044311,37.525000,34.402222,33.797000,38.526822,36.997831,36.634028,38.982737,34.437352,
40.043000,38.219503,34.840000,36.943964,36.079000,36.121275,36.347415,36.515000,36.716806,34.475914,33.841387,38.495000,
34.962000,38.415564,38.283047,38.233972,36.890096,35.205810,36.854875,33.327703,33.220186,36.902778,33.556000,38.649964,
37.151534,34.196531,34.884267,33.662869,33.523694,33.558017,35.603513,38.501258,38.121739,33.536894,36.721083,36.822926,
38.266428,37.016528,35.505833,32.628208,37.314139,37.780653,32.885847,33.532222,34.219386,33.081050,33.549000,38.599158,
34.233639,37.995478,38.419439,34.146372,35.335267,37.438944,33.746000,35.472556,38.312000,34.841878,38.129641,37.725881,
37.552922,36.082272,38.015372,37.598758,35.734000,32.901867,33.798697,33.383070,33.686000,36.900000,37.837614,33.663325,
33.124000,33.080733,35.833059,36.488468,32.729480,32.411000,32.492658,38.090933,37.016760,36.358628,36.382028,37.663969,
34.255980,36.633240,37.720739,38.887603,38.691786,34.614981,34.324639,34.237645,33.748586,32.674353,35.028281,35.862569,
34.426361,36.175833,37.545869,33.268447,33.678151,36.913166,36.540942,37.015026,38.277972,37.931547,36.625626,34.291331,
34.256150,34.269031,33.595736,34.214197,34.592310,34.513611,40.028778,34.142911,40.625499,41.577778,38.672722,38.508333,
38.636111,36.570101,34.405556,34.672222,34.913472,34.138104,34.883472,38.797944,41.802476,33.552810,33.899914,33.664747,
33.756308,33.462405,38.192386,38.249622,39.386632,33.621667,38.773409,38.033386,37.932180,37.755597,39.210667,34.112042,
36.456728,37.255333,37.718167,33.985350,34.759475,35.659128,36.376917,40.604467,41.798331,41.533989]

Longitudes =[-119.732000,-120.112906,-121.793000,-121.726000,-119.281862,-121.776385,-120.590980,-122.165408,-118.894000,
-119.082211,-119.181000,-121.824431,-120.733870,-122.171000,-119.851408,-121.703000,-115.448000,-115.614000,-121.773772,
-119.573000,-119.894900,-119.779000,-121.117000,-116.112000,-116.424000,-119.690000,-121.908000,-121.364000,-120.314000,
-121.546075,-119.152000,-122.024800,-119.223000,-117.199000,-118.405471,-114.558000,-121.545000,-120.384000,-119.504120,
-120.387000,-115.415835,-121.346000,-121.456019,-117.336983,-117.135000,-122.064000,-121.659730,-121.427000,-117.320000,
-116.242000,-122.866000,-120.661783,-121.257000,-119.959300,-116.382000,-120.754227,-120.433948,-119.119000,-118.439000,
-117.115000,-122.153481,-117.228269,-122.543000,-120.079239,-122.082000,-117.135000,-119.839000,-115.732067,-121.950000,
-121.223194,-121.187764,-114.723000,-118.318000,-116.973000,-117.721178,-120.512000,-122.410206,-117.813069,-122.421000,
-119.742308,-120.804000,-117.696000,-122.799931,-121.315669,-123.080122,-119.059344,-115.446258,-119.673800,-121.529300,
-120.480308,-121.472372,-120.880819,-118.929000,-119.869484,-121.809000,-122.280000,-119.200000,-116.938000,-118.476886,
-121.968000,-118.789167,-118.094000,-122.813886,-121.996863,-120.381811,-123.088704,-119.737329,-122.162000,-122.354964,
-116.642000,-121.763942,-120.958000,-121.084455,-121.291248,-121.510000,-121.691889,-117.263514,-116.478729,-122.004000,
-120.548000,-121.786911,-121.790616,-122.116994,-120.731665,-118.778437,-121.362693,-115.944842,-115.580117,-121.741931,
-117.037000,-121.218872,-121.636330,-118.230203,-116.979861,-114.558108,-116.155750,-117.031661,-119.212587,-121.978528,
-121.674455,-115.992803,-119.389028,-121.467934,-122.616464,-120.186394,-119.691144,-116.939281,-120.386700,-122.180150,
-117.143142,-114.633889,-118.992439,-116.975697,-115.916000,-121.540406,-119.196922,-122.467656,-122.658719,-117.985797,
-120.735652,-121.138511,-116.258000,-120.648142,-122.499000,-120.212736,-121.386323,-121.475517,-120.779285,-119.093178,
-122.020278,-122.053233,-119.749000,-117.250458,-118.094792,-114.719385,-116.306000,-121.813000,-122.140739,-117.093383,
-115.803000,-115.685700,-119.255846,-117.919428,-117.139488,-115.197000,-114.826164,-122.526703,-120.148802,-117.943869,
-120.229850,-121.885033,-117.218463,-121.934847,-120.852101,-121.102908,-122.013808,-118.032492,-119.104875,-116.865853,
-116.252903,-115.044381,-120.560033,-119.503700,-118.517583,-120.360270,-120.754531,-116.365050,-116.272921,-121.823497,
-121.882096,-121.537043,-121.740989,-122.302714,-121.537887,-118.570044,-118.382905,-118.849319,-116.158761,-118.644769,
-118.127464,-115.510556,-122.155750,-118.366320,-122.310887,-122.838125,-121.811722,-120.799720,-120.793056,-121.786499,
-119.715000,-120.513056,-120.464778,-116.213508,-116.810247,-121.611361,-121.996159,-117.043302,-117.171325,-116.955121,
-117.197142,-117.586497,-121.510339,-121.555528,-121.835263,-117.585278,-119.791930,-121.701247,-121.397461,-121.266153,
-122.168889,-117.185700,-121.344388,-122.370800,-122.197111,-117.656528,-117.991997,-117.636925,-119.037972,-124.243186,
-122.463425,-122.532279]

#show the weather stations
# plt.scatter(Longitudes, Latitudes)
# plt.grid()
# plt.show()

latStatinMin = np.min(Latitudes)
latStatinMax = np.max(Latitudes)
lngStatinMin = np.min(Longitudes)
lngStatinMax = np.max(Longitudes)

#Weather Data
ToplevelFolder = 'WEATHER'
MonthFolders = ['dailyStnsjan','dailyStnsfeb','dailyStnsmar','dailyStnsapr',
'dailyStnsmay','dailyStnsjun','dailyStnsjul','dailyStnsaug','dailyStnssep', 'dailyStnsoct', 'dailyStnsnov', 'dailyStnsdec']

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

#Weather data must exist at root directory in order for this file pattern to work
#Function determines weather CSV path and loads panda data frame from date and station ID number
def GetWeatherCsv(year, month, stationIdNumber):
    stationIdString = ''
    if stationIdNumber < 10:
        stationIdString = f'00{int(float(str(stationIdNumber)))}'
    if stationIdNumber >= 10 and stationIdNumber < 100:
        stationIdString = f'0{int(float(str(stationIdNumber)))}'
    if stationIdNumber >= 100:
        stationIdString = f'{int(float(str(stationIdNumber)))}'

    return pd.read_csv(f'dailyStns{year}/{MonthFolders[month-1]}/{months[month - 1]}daily{stationIdString}.csv', header=None, delimiter=',')

#Match Index by StationID-1 = index zero based for Latitude and Longitude
#Just hardcoding this for now to perform the rest of the data testing
file_ca_list_local = [ "fire_ca_2022.csv"]
ca_2022 = gen.load_fire_ca(file_ca_list_local)

firstIndex = ca_2022[0]
rawData = pd.read_csv(file_ca_list_local[0], delimiter=';')

values = rawData.values
# Row 0 is the headers
headers = ['IncidentId', 'UniqueId', 'Name', 'Location' ,'Latitude', 'Longitude',
 'AcresBurnedDisplay', 'PercentContainedDisplay', 'ExternalIncidentLink',
 'CountiesList', 'UpdatedDate', 'StartedDate', 'AdminUnit',
 'IncidentTypeDisplay', 'Url', 'IsActive', 'N']

print(headers)

#grid california by 2 degrees

californiaGrids = [[42, 40, -126, -124],
[42, 40, -124, -122],
[42, 40, -122, -120],
[40, 38, -124, -122],
[40, 38, -122, -120],
[40, 38, -120, -118],
[38, 36, -124, -122],
[38, 36, -122, -120],
[38, 36, -120, -118],
[38, 36, -118, -116],
[36, 34, -122, -120],
[36, 34, -120, -118],
[36, 34, -118, -116],
[36, 34, -116, -114],
[34, 32, -120, -118],
[34, 32, -118, -116],
[34, 32, -116, -114]]


#=============================================================
# Originally I used 15 minute intervals for gridding the state of california, but there were edge cases where a station didn't exist
# So I went back to 2 degrees and I am just using the first one that is found
#=============================================================


#Find stations
# Use 15 minute intervals for now, to build grid
# Latitudes are only positive in california
#gen.create_grid(round(abs(gen.ca_max_lat-gen.ca_min_lat)*4),round(abs(gen.ca_max_long-gen.ca_min_long)*4))

# californiaGrids15 = []
# id = 0
# for index, grid2Degree in enumerate(californiaGrids): 
#     print(index)
#     # californiaGrids15.append(gen.create_grid(index*16,4,4,grid2Degree[0],grid2Degree[1],grid2Degree[2],grid2Degree[3]))
#     num_lat = 4
#     num_long = 4
#     max_lat = grid2Degree[0]
#     min_lat = grid2Degree[1]
#     max_long = grid2Degree[2]
#     min_long = grid2Degree[3]
#     delta_lat = np.abs(max_lat - min_lat)/num_lat
#     delta_long = np.abs(max_long - min_long)/num_long
#     #id = 0
#     for i in range(num_lat):
#         for j in range(num_long):
#             grid_min_lat = min_lat + i*delta_lat
#             grid_max_lat = grid_min_lat + delta_lat
#             grid_min_long = min_long + j*delta_long
#             grid_max_long = grid_min_long + delta_long
#             californiaGrids15.append(gen.Grid(id, grid_min_lat, grid_max_lat, grid_min_long, grid_max_long))
#             id += 1

# stationIdsForGrids = np.zeros(len(californiaGrids15))
# found = 0

# for grid15 in californiaGrids15:
#     #print(grid15.output)
#     #locate first Station really need to compare distance or do average
#     foundStation = False
#     for index in range(len(Latitudes)):
#         lat = Latitudes[index]
#         lng = Longitudes[index]
#         if lat <= grid15.max_lat and lat >= grid15.min_lat and lng >= grid15.min_long and lng <= grid15.max_long and foundStation == False:
#             print(f'StationID is {index + 1} for bounds {grid15.output}')
#             stationIdsForGrids[index] = index + 1
#             found = found + 1
#             foundStation = True
#     if foundStation == False:
#         testing = grid15

stationIdsForGrids = np.zeros(len(californiaGrids))
found = 0
californiaGrids2Degrees = []

#redid gridding due to no stations found when using 15 minute intervals
for grid2 in californiaGrids:
    #locate first Station really need to compare distance or do average
    foundStation = False
    for index in range(len(Latitudes)):
        lat = Latitudes[index]
        lng = Longitudes[index]
        if lat <= grid2[0] and lat >= grid2[1] and lng >= grid2[2] and lng <= grid2[3] and foundStation == False:
            gridToAdd = gen.Grid(found, grid2[1], grid2[0], grid2[2], grid2[3])
            californiaGrids2Degrees.append(gridToAdd)
            print(f'StationID is {index + 1} for bounds {gridToAdd.output}')
            stationIdsForGrids[found] = index + 1
            found = found + 1
            foundStation = True
    if foundStation == False:
        #Station was not found for this grid
        print(f'No station was found for {grid2[1]}, {grid2[0]}, {grid2[2]}, {grid2[3]}')


# def FindMyGrid(testLatitude, testLongitude):
#     lat = testLatitude
#     lng = testLongitude
#     for index, checkGrid in enumerate(californiaGrids15):
#             if lat <= checkGrid.max_lat and lat >= checkGrid.min_lat and lng >= checkGrid.min_long and lng <= checkGrid.max_long:
#                 print(f'{checkGrid.output}')
#                 return checkGrid.grid_id

# iterates for grids to locate id of grid that contains coordinates
def FindMyGrid(testLatitude, testLongitude):
    lat = testLatitude
    lng = testLongitude
    for index, checkGrid in enumerate(californiaGrids2Degrees):
            if lat <= checkGrid.max_lat and lat >= checkGrid.min_lat and lng >= checkGrid.min_long and lng <= checkGrid.max_long:
                print(f'{checkGrid.output}')
                return checkGrid.grid_id

print('printing HEAD')
print(rawData.head())

#This is just done locally for now, need to build this into a function
gridLats = rawData['Latitude'].values
gridLongs = rawData['Longitude'].values
gridTimeStart = rawData['StartedDate'].values
gridTimeEnd = rawData['UpdatedDate'].values

#Test getting weather data for first input
WhatGridIsThis = FindMyGrid(gridLats[0], gridLongs[0])

#Time formatting is different for the start and end
startTime = datetime.strptime(gridTimeStart[0], '%Y-%m-%d')
endTime = datetime.strptime(gridTimeEnd[0], '%Y-%m-%d %H:%M:%S')

stationToTest = stationIdsForGrids[WhatGridIsThis]

weatherDataDay1 = GetWeatherCsv(startTime.year, startTime.month, stationToTest)

#this is just here to force a break point
b = 5
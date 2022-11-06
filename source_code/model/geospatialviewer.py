import geopandas as gpd
import shapely.wkt

import matplotlib.pyplot as plt
import matplotlib as mpl

import math
import time
import os.path
from datetime import datetime, date

df = gpd.read_file('D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\SpatialData\\California_Fire_Perimeters_(all).geojson')
# print(dfAll.head())

#df = gpd.read_file('D:\\MastersAI\\Stevens\\AppliedMachineLearning\\CPE_695WS\\FinalProject\\SpatialData\\California_Fire_Perimeters_large.geojson')

df.plot()

fig, ax = plt.subplots(figsize=(10,10))
df.plot(ax=ax, **{'edgecolor':'black', 'facecolor':'white'})

fig.show()

# s = gpd.GeoSeries.to_crs(df,crs=4326)

# s.centroid.plot(ax=ax, c='blue')

test = 0
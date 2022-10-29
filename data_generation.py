import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime, date, timedelta

ca_min_lat =  32.5121
ca_max_lat = 42.0126
ca_min_long = -124.6509
ca_max_long= -114.1315
file_ca_list = ["fire_ca_2013.csv", "fire_ca_2014.csv", "fire_ca_2015.csv", "fire_ca_2016.csv", "fire_ca_2017.csv",
                "fire_ca_2018.csv", "fire_ca_2019.csv", "fire_ca_2020.csv", "fire_ca_2021.csv", "fire_ca_2022.csv"]
def load_fire_ca(file_list):
    fire_data = []
    for f in range(len(file_list)):
        data = pandas.read_csv(file_list[f], header=0, delimiter=';')
        fire_data.append(data)

    return fire_data

class Grid:
    def __init__(self, grid_id, min_lat, max_lat, min_long, max_long):
        self.grid_id = grid_id
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_long = min_long
        self.max_long = max_long
    def to_string(self):
        return str(self.grid_id) +','+str(self.min_lat)+','+str(self.max_lat)+','+str(self.min_long)+','+str(self.max_long)

def create_grid(num_lat, num_long):
    grids = []
    delta_lat = (ca_max_lat - ca_min_lat)/num_lat
    delta_long = (ca_max_long - ca_min_long)/num_long
    id = 0
    for i in range(num_lat):
        for j in range(num_long):
            grid_min_lat = ca_min_lat + i*delta_lat
            grid_max_lat = grid_min_lat + delta_lat
            grid_min_long = ca_min_long + j*delta_long
            grid_max_long = grid_min_long + delta_long
            grids.append(Grid(id, grid_min_lat, grid_max_lat, grid_min_long, grid_max_long))
            id += 1
    return grids

def match_weathersts_to_grid(grid, stations):
    grid_station = {}
    sts = pandas.read_excel(stations, header=0)
    sts = sts.drop([261])
    sts.iloc[:, 8] = pandas.to_datetime(sts.iloc[:, 8])
    sts = sts.loc[sts.iloc[:,7] == 'Active']
    sts = sts.loc[sts.iloc[:,8]< np.datetime64('2013-01-01')]

    for g in grid:
        for i in range(len(sts)):
            if sts.iloc[i,4]>= g.min_lat and sts.iloc[i,4] <g.max_lat and sts.iloc[i,5]>= g.min_long and sts.iloc[i,5] <g.max_long:
                if(g.grid_id not in grid_station):
                    grid_station[g.grid_id] = [int(sts.iloc[i,0])]
                else:
                    grid_station[g.grid_id].append(int(sts.iloc[i,0]))
        if(g.grid_id not in grid_station):
            c_lat = (g.max_lat + g.min_lat)/2.0
            c_long = (g.max_long + g.min_long)/2.0
            station_id = 0
            dist = 1e10
            for i in range(len(sts)):
                dist_tmp = math.sqrt((c_lat - sts.iloc[i,4])**2 + (c_long-sts.iloc[i,5])**2)
                if(dist_tmp<dist):
                    dist = dist_tmp
                    station_id = sts.iloc[i,0]
            grid_station[g.grid_id] = [int(station_id)]
    return grid_station

#      1.  Station Id
#      2.  Date
#      3.  Julian Date
#      4.  QC for Solar Radiation Average
#      5.  Solar Radiation Average   (Ly/day)   (W/m≤)
#      6.  QC for Average Soil Temperature
#      7.  Average Soil Temperature   (∞F)   (∞C)
#      8.  QC for Maximum Air Temperature
#      9.  Maximum Air Temperature   (∞F)   (∞C)
#      10. QC for Minimum Air Temperature
#      11. Minimum Air Temperature   (∞F)   (∞C)
#      12. QC for Average Air Temperature
#      13. Average Air Temperature   (∞F)   (∞C)
#      14. QC for Average Vapor Pressure
#      15. Average Vapor Pressure   (mBars)   (kPa)
#      16. QC for Average Wind Speed
#      17. Average Wind Speed   (mph)   (m/s)
#      18. QC for Precipitation
#      19. Precipitation   (in)   (mm)
#      20. QC for Maximum Relative Humidity
#      21. Maximum Relative Humidity   (%)
#      22. QC for Minimum Relative Humidity
#      23. Minimum Relative Humidity   (%)
#      24. QC for Reference ETo
#      25. Reference ETo   (in)   (mm)
#      26. QC for Average Relative Humidity
#      27. Average Relative Humidity   (%)
#      28. QC for Dew Point
#      29. Dew Point   (∞F)   (∞C)
#      30. QC for Wind Run
#      31. Wind Run   (miles)   (km)

def extract_weather_2013(station):
    stationIdString = str(station).zfill(3)
    file_name = f'./weather_data/dailyStns2013/2013daily{stationIdString}.csv'
    df = pandas.read_csv(file_name, header=None)
    data = {}
    for i in range(len(df)):
        date_format = datetime.strptime(df.iloc[i,1], '%m/%d/%Y').date()
        data[date_format] = {"solar_rad": df.iloc[i,4],
                            "soil_temp": df.iloc[i,6],
                            "max_air_temp": df.iloc[i,8],
                            "min_air_temp": df.iloc[i,10],
                            "aver_air_temp": df.iloc[i,12],
                            "aver_vapor_press": df.iloc[i,14],
                            "aver_wind_speed": df.iloc[i,16],
                            "precipitation": df.iloc[i,18],
                            "max_humidity": df.iloc[i,20],
                            "min_humidity": df.iloc[i,22],
                            "eto": df.iloc[i,24],
                            "aver_humidity": df.iloc[i, 26],
                            "dew_point": df.iloc[i,28],
                            "wind_run": df.iloc[i,30]
                            }
    return data

  # A   1.  	Station Id
  # B   2. 	    Date
  # C   3. 	    Julian Date
  # D   4.  	Reference ETo   (in)   (mm)
  # E   5.  	QC for Reference ETo
  # F   6.  	Precipitation   (in)   (mm)
  # G   7.  	QC for Precipitation
  # H   8.  	Solar Radiation Average   (Ly/day)   (W/m≤)
  # I   9.  	QC for Solar Radiation Average
  # J   10. 	Average Vapor Pressure   (mBars)   (kPa)
  # K   11. 	QC for Average Vapor Pressure
  # L   12. 	Maximum Air Temperature   (∞F)   (∞C)
  # M   13. 	QC for Maximum Air Temperature
  # N   14. 	Minimum Air Temperature   (∞F)   (∞C)
  # O   15. 	QC for Minimum Air Temperature
  # P   16. 	Average Air Temperature   (∞F)   (∞C)
  # Q   17. 	QC for Average Air Temperature
  # R   18. 	Maximum Relative Humidity   (%)
  # S   19. 	QC for Maximum Relative Humidity
  # T   20. 	Minimum Relative Humidity   (%)
  # U   21. 	QC for Minimum Relative Humidity
  # V   22. 	Average Relative Humidity   (%)
  # W   23. 	QC for Average Relative Humidity
  # X   24. 	Dew Point   (∞F)   (∞C)
  # Y   25. 	QC for Dew Point
  # Z   26. 	Average Wind Speed   (mph)   (m/s)
  # AA  27. 	QC for Average Wind Speed
  # AB  28. 	Wind Run   (miles)   (km)
  # AC  29. 	QC for Wind Run
  # AD  30. 	Average Soil Temperature   (∞F)   (∞C)
  # AE  31. 	QC for Average Soil Temperature
def extract_weather(year, station):
    stationIdString = str(station).zfill(3)
    if(year=="2016" or year=="2021"):
        file_name = f'./weather_data/dailyStns{year}/daily{stationIdString}.csv'
    else:
        file_name = f'./weather_data/dailyStns{year}/{year}daily{stationIdString}.csv'
    df = pandas.read_csv(file_name, header=None)
    data = {}
    for i in range(len(df)):
        date_format = datetime.strptime(df.iloc[i, 1], '%m/%d/%Y').date()
        data[date_format] = {"eto": df.iloc[i, 3],
                             "precipitation": df.iloc[i, 5],
                             "solar_rad": df.iloc[i, 7],
                             "aver_vapor_press": df.iloc[i, 9],
                             "max_air_temp": df.iloc[i, 11],
                             "min_air_temp": df.iloc[i, 13],
                             "aver_air_temp": df.iloc[i, 15],
                             "max_humidity": df.iloc[i, 17],
                             "min_humidity": df.iloc[i, 19],
                             "aver_humidity": df.iloc[i, 21],
                             "dew_point": df.iloc[i, 23],
                             "aver_wind_speed": df.iloc[i, 25],
                             "wind_run": df.iloc[i, 27],
                             "soil_temp": df.iloc[i, 29]
                             }
    return data

def extract_weather_2022(station):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']
    stationIdString = str(station).zfill(3)
    data = {}
    for m in months:
        file_name = f'./weather_data/dailyStns2022/dailyStns{m}/{m}daily{stationIdString}.csv'
        df = pandas.read_csv(file_name, header=None)
        for i in range(len(df)):
            date_format = datetime.strptime(df.iloc[i, 1], '%m/%d/%Y').date()
            data[date_format] = {"eto": df.iloc[i, 3],
                             "precipitation": df.iloc[i, 5],
                             "solar_rad": df.iloc[i, 7],
                             "aver_vapor_press": df.iloc[i, 9],
                             "max_air_temp": df.iloc[i, 11],
                             "min_air_temp": df.iloc[i, 13],
                             "aver_air_temp": df.iloc[i, 15],
                             "max_humidity": df.iloc[i, 17],
                             "min_humidity": df.iloc[i, 19],
                             "aver_humidity": df.iloc[i, 21],
                             "dew_point": df.iloc[i, 23],
                             "aver_wind_speed": df.iloc[i, 25],
                             "wind_run": df.iloc[i, 27],
                             "soil_temp": df.iloc[i, 29]
                             }
    return data

def match_fire_incident_to_grid(grid, fire_incidents):
    grid_incident = {}
    for incident in fire_incidents:
        for i in range(len(incident)):
            inc_lat = incident.iloc[i,4]
            inc_long = incident.iloc[i,5]
            start_date = incident.iloc[i,11]
            date_format = datetime.strptime(start_date, '%Y-%m-%d').date()
            arce_burn = incident.iloc[i,6]
            # mark = 0
            for g in grid:
                if inc_lat >= g.min_lat and inc_lat < g.max_lat and inc_long >= g.min_long and inc_long < g.max_long:
                    if(g.grid_id not in grid_incident):
                        grid_incident[g.grid_id]={date_format:[arce_burn]}
                    else:
                        if(date_format not in grid_incident[g.grid_id]):
                            grid_incident[g.grid_id][date_format] = [arce_burn]
                        else:
                            grid_incident[g.grid_id][date_format].append(arce_burn)
                    # mark += 1
                    break
            # if(mark==0):
            #     print(incident.iloc[i,0], inc_lat, inc_long)
    return grid_incident


fires = load_fire_ca(file_ca_list)
grid = create_grid(10,10)
fire_grid = match_fire_incident_to_grid(grid,fires)
station_grid = match_weathersts_to_grid(grid, './weather_data/CIMIS Stations List (January20).xlsx')
grid_weather = {}

for g, s in station_grid.items():
    grid_weather[g]={}
    weather = extract_weather_2013(s[0])
    for i in range(2014, 2022):
        weather.update(extract_weather(str(i), s[0]))
    weather.update(extract_weather_2022(s[0]))
    if(len(s)>1):
        dates = list(weather.keys())
        weather_feat = weather[dates[0]].keys()
        for i in range(1, len(s)):
            tmp_weather = extract_weather_2013(s[i])
            for y in range(2014, 2022):
                tmp_weather.update(extract_weather(str(y), s[i]))
            tmp_weather.update(extract_weather_2022(s[i]))
            for d in dates:
                print(d)
                for f in weather_feat:
                    print(f)
                    print(type(weather[d][f]),'****', type(tmp_weather[d][f]))
                    weather[d][f] += tmp_weather[d][f]
        for d in dates:
            for f in weather_feat:
                weather[d][f] /= len(s)

    grid_weather[g] = weather


# weather = extract_weather_2013(147)
# for d in weather.keys():
#     for k,v in weather[d].items():
#         print(d, k, type(weather[d][k]), v)

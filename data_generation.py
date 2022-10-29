import pandas
import matplotlib.pyplot as plt
import numpy as np
import math
from datetime import datetime, date, timedelta
import os.path

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
def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

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
    data = {}
    if(os.path.isfile(file_name)):
        lines = open(file_name, 'r').readlines()
        for line in lines:
            line = line.strip().split(',')
            line =[l.strip() for l in line]
            date_format = datetime.strptime(line[1], '%m/%d/%Y').date()
            data[date_format] = {}
            data[date_format]["solar_rad"] = float(line[4]) if(is_float(line[4])) else 'NaN'
            data[date_format]["soil_temp"] = float(line[6]) if (is_float(line[6])) else 'NaN'
            data[date_format]["max_air_temp"] = float(line[8]) if (is_float(line[8])) else 'NaN'
            data[date_format]["min_air_temp"] = float(line[10]) if (is_float(line[10])) else 'NaN'
            data[date_format]["aver_air_temp"] = float(line[12]) if (is_float(line[12])) else 'NaN'
            data[date_format]["aver_vapor_press"] = float(line[14]) if (is_float(line[14])) else 'NaN'
            data[date_format]["aver_wind_speed"] = float(line[16]) if (is_float(line[16])) else 'NaN'
            data[date_format]["precipitation"] = float(line[18]) if (is_float(line[18])) else 'NaN'
            data[date_format]["max_humidity"] = float(line[20]) if (is_float(line[20])) else 'NaN'
            data[date_format]["min_humidity"] = float(line[22]) if (is_float(line[22])) else 'NaN'
            data[date_format]["eto"] = float(line[24]) if (is_float(line[24])) else 'NaN'
            data[date_format]["aver_humidity"] = float(line[26]) if (is_float(line[26])) else 'NaN'
            data[date_format]["dew_point"] = float(line[28]) if (is_float(line[28])) else 'NaN'
            data[date_format]["wind_run"] = float(line[30]) if (is_float(line[30])) else 'NaN'

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
    data = {}
    if(os.path.isfile(file_name)):
        lines = open(file_name, 'r').readlines()
        for line in lines:
            line = line.strip().split(',')
            line = [l.strip() for l in line]
            date_format = datetime.strptime(line[1], '%m/%d/%Y').date()
            data[date_format] = {}
            data[date_format]["eto"] = float(line[3]) if (is_float(line[3])) else 'NaN'
            data[date_format]["precipitation"] = float(line[5]) if (is_float(line[5])) else 'NaN'
            data[date_format]["solar_rad"] = float(line[7]) if (is_float(line[7])) else 'NaN'
            data[date_format]["aver_vapor_press"] = float(line[9]) if (is_float(line[9])) else 'NaN'
            data[date_format]["max_air_temp"] = float(line[11]) if (is_float(line[11])) else 'NaN'
            data[date_format]["min_air_temp"] = float(line[13]) if (is_float(line[13])) else 'NaN'
            data[date_format]["aver_air_temp"] = float(line[15]) if (is_float(line[15])) else 'NaN'
            data[date_format]["max_humidity"] = float(line[17]) if (is_float(line[17])) else 'NaN'
            data[date_format]["min_humidity"] = float(line[19]) if (is_float(line[19])) else 'NaN'
            data[date_format]["aver_humidity"] = float(line[21]) if (is_float(line[21])) else 'NaN'
            data[date_format]["dew_point"] = float(line[23]) if (is_float(line[23])) else 'NaN'
            data[date_format]["aver_wind_speed"] = float(line[25]) if (is_float(line[25])) else 'NaN'
            data[date_format]["wind_run"] = float(line[27]) if (is_float(line[27])) else 'NaN'
            data[date_format]["soil_temp"] = float(line[29]) if (is_float(line[29])) else 'NaN'
    return data


def extract_weather_2022(station):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep']
    stationIdString = str(station).zfill(3)
    data = {}
    for m in months:
        file_name = f'./weather_data/dailyStns2022/dailyStns{m}/{m}daily{stationIdString}.csv'
        if(os.path.isfile(file_name)):
            lines = open(file_name, 'r').readlines()
            for line in lines:
                line = line.strip().split(',')
                line = [l.strip() for l in line]
                date_format = datetime.strptime(line[1], '%m/%d/%Y').date()
                data[date_format] = {}
                data[date_format]["eto"] = float(line[3]) if (is_float(line[3])) else 'NaN'
                data[date_format]["precipitation"] = float(line[5]) if (is_float(line[5])) else 'NaN'
                data[date_format]["solar_rad"] = float(line[7]) if (is_float(line[7])) else 'NaN'
                data[date_format]["aver_vapor_press"] = float(line[9]) if (is_float(line[9])) else 'NaN'
                data[date_format]["max_air_temp"] = float(line[11]) if (is_float(line[11])) else 'NaN'
                data[date_format]["min_air_temp"] = float(line[13]) if (is_float(line[13])) else 'NaN'
                data[date_format]["aver_air_temp"] = float(line[15]) if (is_float(line[15])) else 'NaN'
                data[date_format]["max_humidity"] = float(line[17]) if (is_float(line[17])) else 'NaN'
                data[date_format]["min_humidity"] = float(line[19]) if (is_float(line[19])) else 'NaN'
                data[date_format]["aver_humidity"] = float(line[21]) if (is_float(line[21])) else 'NaN'
                data[date_format]["dew_point"] = float(line[23]) if (is_float(line[23])) else 'NaN'
                data[date_format]["aver_wind_speed"] = float(line[25]) if (is_float(line[25])) else 'NaN'
                data[date_format]["wind_run"] = float(line[27]) if (is_float(line[27])) else 'NaN'
                data[date_format]["soil_temp"] = float(line[29]) if (is_float(line[29])) else 'NaN'
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

def daterange(date1, date2):
    date_list = []
    for n in range(int ((date2 - date1).days)+1):
        date_list.append (date1 + timedelta(n))
    return date_list

start_dt = date(2013, 1, 1)
end_dt = date(2022, 9, 30)

dates = daterange(start_dt, end_dt)

weather_feat = ["eto", "precipitation", "solar_rad","aver_vapor_press", "max_air_temp",
                "min_air_temp", "aver_air_temp", "max_humidity", "min_humidity", "aver_humidity",
                "dew_point", "aver_wind_speed", "wind_run", "soil_temp"]

fires = load_fire_ca(file_ca_list)
grid = create_grid(10,10)
fire_grid = match_fire_incident_to_grid(grid,fires)
station_grid = match_weathersts_to_grid(grid, './weather_data/CIMIS Stations List (January20).xlsx')
grid_weather = {}

len_valid_features = {}
for g, s in station_grid.items():
    print(g,s)
    grid_weather[g]={}
    len_valid_features[g] ={}
    weather_first_sts = extract_weather_2013(s[0])
    for i in range(2014, 2022):
        weather_first_sts.update(extract_weather(str(i), s[0]))
    weather_first_sts.update(extract_weather_2022(s[0]))

    for d in dates:
        if(d in weather_first_sts):
            grid_weather[g][d] = weather_first_sts[d]
        else:
            grid_weather[g][d] = {}
            for f in weather_feat:
                grid_weather[g][d][f] = "NaN"
    for d in dates:
        len_valid_features[g][d] = {}
        for f in weather_feat:
            if grid_weather[g][d][f] != "NaN":
                len_valid_features[g][d][f] = 1
            else:
                len_valid_features[g][d][f] = 0
    if(len(s)>1):
        for i in range(1, len(s)):
            tmp_weather = extract_weather_2013(s[i])
            for y in range(2014, 2022):
                tmp_weather.update(extract_weather(str(y), s[i]))
            tmp_weather.update(extract_weather_2022(s[i]))
            for d in dates:
                for f in weather_feat:
                    if d in tmp_weather:
                        if(grid_weather[g][d][f] != "NaN" and tmp_weather[d][f] != "NaN"):
                            grid_weather[g][d][f] += tmp_weather[d][f]
                            len_valid_features[g][d][f] += 1
                        elif(grid_weather[g][d][f] == "NaN" and tmp_weather[d][f] != "NaN"):
                            grid_weather[g][d][f] = tmp_weather[d][f]
                            len_valid_features[g][d][f] += 1
                        else:
                            continue

        for d in dates:
            for f in weather_feat:
                if(len_valid_features[g][d][f] != 0 and grid_weather[g][d][f] != "NaN"):
                    grid_weather[g][d][f] /= len_valid_features[g][d][f]

for g in grid_weather.keys():
    for d in dates:
        if(g in fire_grid and d in fire_grid[g]):
            grid_weather[g][d]['has_fire'] = 1
        else:
            grid_weather[g][d]['has_fire'] = 0
weather_feat = weather_feat + ['has_fire']

header = ['grid_id', 'date'] + weather_feat
header = ','.join(header)
file_out = open('train_data.csv', 'w')
file_out.write(header+'\n')
for g in grid_weather.keys():
    for d in dates:
        s = str(g)+','+str(d)+','
        for f in range(len(weather_feat)):
            s += str(grid_weather[g][d][weather_feat[f]])+','
        s = s[:len(s)-1]
        file_out.write(s+'\n')
file_out.close()
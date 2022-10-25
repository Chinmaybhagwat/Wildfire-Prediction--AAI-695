import pandas
import matplotlib.pyplot as plt
import numpy as np
ca_min_lat =  32.5121
ca_max_lat = 42.0126
ca_min_long = -124.6509
ca_max_long= -114.1315
file_ca_list = ["fire_ca_2013.csv", "fire_ca_2014.csv", "fire_ca_2015.csv", "fire_ca_2016.csv", "fire_ca_2017.csv",
                "fire_ca_2018.csv", "fire_ca_2019.csv", "fire_ca_2020.csv", "fire_ca_2021.csv", "fire_ca_2022.csv"]
def load_fire_ca(file_list):
    fire_data = []
    for f in range(len(file_list)):
        data = pandas.read_csv(file_list[f], header=None, delimiter=';')
        fire_data.append(data)
        print(data.shape)

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
    for g in grid:
        for i in range(len(sts)):
            if sts.iloc[i,4]>= g.min_lat and sts.iloc[i,4] <g.max_lat and sts.iloc[i,5]>= g.min_long and sts.iloc[i,5] <g.max_long:
                if(g.grid_id not in grid_station):
                    grid_station[g.grid_id] = [sts.iloc[i,0]]
                else:
                    grid_station[g.grid_id].append(sts.iloc[i,0])
    return grid_station

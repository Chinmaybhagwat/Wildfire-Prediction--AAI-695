import math as Math
import time
import os.path
from datetime import datetime, date

import numpy as np
import pandas

#meters geodetic 1984 radius
RadiusWgs1984 = 6356752.3142

DegreesToRadians = Math.pi/180.0
RadiansToDegrees = 180/Math.pi

class GeoSpatial:

    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
        phi1 = lat1 * DegreesToRadians
        phi2 = lat2 * DegreesToRadians
        deltaPhi = (lat2-lat1) * DegreesToRadians
        deltaLamba = (lon2-lon1) * DegreesToRadians
        a = Math.sin(deltaPhi/2) * Math.sin(deltaPhi/2) + Math.cos(phi1) * Math.cos(phi2) *  Math.sin(deltaLamba/2) * Math.sin(deltaLamba/2)
        c = Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
        d = RadiusWgs1984 * c        
        return d

    @staticmethod
    def equirectanglurProjection(lat1: float, lon1: float, lat2: float, lon2: float):      
        phi1 = lat1 * DegreesToRadians
        phi2 = lat2 * DegreesToRadians  	
        lamba1 = lon1 * DegreesToRadians
        lamba2 = lon2 * DegreesToRadians  
        x = (lamba2-lamba1) * Math.cos((phi1+phi2)/2)
        y = (phi2-phi1)
        d = Math.sqrt(x*x + y*y) * RadiusWgs1984
        return d

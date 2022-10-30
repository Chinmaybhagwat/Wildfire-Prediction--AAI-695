========================================================
CIMIS (California Irrigation Management Information System)
DAILY AND HOURLY FTP REPORTS (EXTRACTS)

Department of Water Resources
Water Use Efficiency Office
901 P Street, Third Floor 
P.O. Box 942836
Sacramento, CA 94236-0001 

Bekele Temesgen
(916) 651-9679
temesgen@water.ca.gov 
========================================================

Overview:
FTP files provide CIMIS weather data to the public via text files in 
"comma separated values" (CSV) format. The data files may be imported into 
spreadsheet programs like Excel or into databases like Access or Oracle.

Files:
Daily and Hourly data extract files are named using the following pattern:

     dailyXXX.csv          hourlyXXX.csv

The "XXX" represents the station number the file provides data for. 
Zip files are used to compress the CSV files for faster downloads. 

For both "daily" and "hourly" one extract file exists for every active 
station. Each file is updated throughout the day - with each upload 
happening every hour for data from 2 hours previous. 

Folders:
"annual" includes daily and hourly data organized by year, then station. 
Updated on the 2nd day of the month.

 "daily" includes seven days of data in each extract file. The seven day 
period is based on yesterday's date; therefore, yesterday's and six days 
prior to yesterday should exist in each extract file.  
Also, under "daily" are two other data options:
"dailyAllStns.zip" provides all the "dailyxxx" files - english and metric -  in one zip file,
"DayYrEToxxx.csv" files provide ETo data for the prior 365 days, for each station.

"hourly" includes seven days of data plus today's most recently uploaded 
hours in each extract file. Data for today and seven days previous 
should exist in each extract file.
Also, under "hourly" is a file named "hourlyAllStns.zip" which includes 
all "hourlyxxx" files - english and metric -  in one zip file.

"monthly" includes each month's daily and hourly data per station. 
Updated on the 2nd day of the month. Includes the last 12 months.

"CIMIS Stations List (February 2017).xlsx" is a list of Station numbers, DWR Regional 
Office, Names, County, Latitude, Longitude, Elevation, Activity Status, Connect date, 
and Disconnect date.  This list is from updated yearly if not more often. 


DAILY Default Order of Data Columns:

letter/number   Sensor/Field   (English Unit)   (Metric Unit)
============================================
  A   1.  	Station Id
  B   2. 	Date
  C   3. 	Julian Date
  D   4.  	Reference ETo   (in)   (mm)
  E   5.  	QC for Reference ETo              
  F   6.  	Precipitation   (in)   (mm)
  G   7.  	QC for Precipitation              
  H   8.  	Solar Radiation Average   (Ly/day)   (W/m²)
  I   9.  	QC for Solar Radiation Average    
  J   10. 	Average Vapor Pressure   (mBars)   (kPa)
  K   11. 	QC for Average Vapor Pressure     
  L   12. 	Maximum Air Temperature   (°F)   (°C)
  M   13. 	QC for Maximum Air Temperature    
  N   14. 	Minimum Air Temperature   (°F)   (°C)
  O   15. 	QC for Minimum Air Temperature    
  P   16. 	Average Air Temperature   (°F)   (°C)
  Q   17. 	QC for Average Air Temperature
  R   18. 	Maximum Relative Humidity   (%)
  S   19. 	QC for Maximum Relative Humidity
  T   20. 	Minimum Relative Humidity   (%)
  U   21. 	QC for Minimum Relative Humidity
  V   22. 	Average Relative Humidity   (%)
  W   23. 	QC for Average Relative Humidity
  X   24. 	Dew Point   (°F)   (°C)
  Y   25. 	QC for Dew Point
  Z   26. 	Average Wind Speed   (mph)   (m/s)
  AA  27. 	QC for Average Wind Speed
  AB  28. 	Wind Run   (miles)   (km)
  AC  29. 	QC for Wind Run
  AD  30. 	Average Soil Temperature   (°F)   (°C)
  AE  31. 	QC for Average Soil Temperature

HOURLY Default Order of Data Columns:

letter/number   Sensor/Field   (English Unit)   (Metric Unit)
===========================================
  A   1.  	Station Id
  B   2.  	Date
  C   3.  	Hour   (PST)
  D   4.  	Julian Date
  E   5.  	Reference ETo   (in)   (mm)
  F   6.  	QC for Reference ETo
  G   7.  	Precipitation   (in)   (mm)
  H   8.  	QC for Precipitation
  I   9.  	Solar Radiation   (Ly/day)   (W/m²)
  J   10. 	QC for Solar Radiation 
  K   11. 	Vapor Pressure   (mBars)   (kPa)
  L   12. 	QC for Vapor Pressure
  M   13. 	Air Temperature   (°F)   (°C)
  N   14. 	QC for Air Temperature
  O   15. 	Relative Humidity   (%)
  P   16. 	QC for Relative Humidity
  Q   17. 	Dew Point   (°F)   (°C)
  R   18. 	QC for Dew Point
  S   19. 	Wind Speed   (mph)   (m/s)
  T   20. 	QC for Wind Speed
  U   21. 	Wind Direction   (0-360)
  V   22. 	QC for Wind Direction
  W   23. 	Soil Temperature   (°F)   (°C)
  X   24. 	QC for Soil Temperature



Please refer to our public website for information on what station number
would be of interest to you. You will likely need to know the City, County, 
Region, or Zip codes of the locations you are interested in. This data can 
be easily obtained from the CIMIS website:    wwwcimis.water.ca.gov

Look under "STATIONS" and select "Station Location Map" for more details.

Note: Precipitation data presented on the CIMIS website may be adjusted 
occassionally to avoid erroneous sprinkler irrigation readings.  FTP Data may 
not include these adjustments. 
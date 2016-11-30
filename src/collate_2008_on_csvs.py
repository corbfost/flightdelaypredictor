import pandas as pd
import numpy as np
import os


dirname = '/Users/cf/Documents/Galvanize/flight_delays/data/2009_on/unzipped_csvs/'
os.chdir(dirname)
extension = ".csv"

# Get dataframe from earlier years to match the columns
df_good = pd.read_csv('/Users/cf/Documents/Galvanize/flight_delays/data/sea_limited_data/2007.csv')
cols = set(df_good.columns.values)


# Loop through csvs, select Seattle, then select relevant columns
bigdf = df_good

for i, item in enumerate(os.listdir(dirname)):  # loop through items in dir
    print "{}% done".format((float(i)/len(os.listdir(dirname)))*100)
    if item.endswith(extension):
        file_name = os.path.abspath(item)
        df = pd.read_csv(file_name)
        df = df.ix[(df['Origin'] == 'SEA') | (df['Dest'] == 'SEA'), :]
        manycols = set(df.columns.values)
        unnecessary_cols = manycols.difference(cols.intersection(manycols))
        df = df.drop(unnecessary_cols, axis=1)
        bigdf = pd.concat((bigdf, df))

# Write 2008 - 2016 to big CSV
bigdf.to_csv('/Users/cf/Documents/Galvanize/flight_delays/data/sea_limited_data/2008_on.csv')

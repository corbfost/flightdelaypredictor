import glob
import pandas as pd


path ='/Users/cf/Documents/Galvanize/flight_delays/data/sea_limited_data'
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
frame = pd.concat(list_)
frame.to_csv('/Users/cf/Documents/Galvanize/flight_delays/data/sea_all_years.csv')

import pandas as pd
import numpy as np
import cPickle as pickle
from datetime import date, datetime, timedelta

def load_pickle(filepath):
    with open(filepath, 'r') as f:
        name = pickle.load(f)
    return name

def picklify(obj, name):
    with open(name, 'w') as f:
        pickle.dump(obj, f)
    print "pickled " + name
    return

print "Loading data"
df = pd.read_csv('./data/sea_all_years.csv')

# Drop unnamed column and NA
df = df.drop('Unnamed: 0', axis=1)
df = df.drop('Unnamed: 0.1', axis=1)

print "Dropping nulls"
df = df.dropna(axis=0, subset=['ArrTime', 'ArrDelay', 'DepDelay', 'DepTime',
                               'ActualElapsedTime', 'CRSElapsedTime', 'Distance'])

print "Processing dates"
# Datetime processing
dates = df.ix[:, ['Year', 'Month', 'DayofMonth']]
dates.columns = ['year', 'month', 'day']
dates = pd.to_datetime(dates, infer_datetime_format=True)
df['Date'] = dates

# Limit to Seattle origins
print "Limiting to Origin = SEA"
df = df.ix[df['Origin'] == 'SEA', :]

# Limit dates after 3rd runway
print "Limiting to dates after 2008-12-01"
df = df.ix[df['Date'] > '2008-12-01', :]

# Load airport delay information
airports = load_pickle('./data/airport_delays.pkl')

# Exclude weather delays
df = df.ix[(pd.isnull(df['WeatherDelay'])) |
                                (df['WeatherDelay'] == 0), :]

# Add airport delay info
df = df.merge(airports, how='left',
                                    left_on='Dest', right_on='Airport')

# Add unique route identifier and group by delays
df['OrDestCarrier'] = df['Origin'] + df['Dest'] + df['UniqueCarrier']
flight_delay_history = df.groupby('OrDestCarrier').mean()['DepDelay'].reset_index()
df = df.merge(flight_delay_history, how='left',
                                    on='OrDestCarrier', suffixes=['','r'])

# Alaska indicator, just for shits.
df['Alaska'] = (df['UniqueCarrier'] == 'AS').astype(int)

# load holiday columns
wint_hol_1day = load_pickle('./data/wint_hol_1day_bef.pkl')
wint_hol_2day = load_pickle('./data/wint_hol_2day_bef.pkl')
fri_bef_mon_holiday = load_pickle('./data/fri_bef_mon_holiday.pkl')

# add indicators:
print "Adding holiday indicators"
df['wint_hol_1day'] = [n in wint_hol_1day for n in df.Date.astype(datetime)]
df['wint_hol_2day'] = [n in wint_hol_2day for n in df.Date.astype(datetime)]
df['fri_bef_mon_holiday'] = [n in fri_bef_mon_holiday for n in df.Date.astype(datetime)]

# final thing - airport latitude and info.
airport_info = pd.read_csv('./data/airports.csv')
df = df.merge(airport_info, how='left', left_on='Dest', right_on='iata')

picklify(df, './data/model_data.pkl')

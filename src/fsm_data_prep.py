import pandas as pd

df = pd.read_csv('./data/sea_all_years.csv')

df = df.drop('Unnamed: 0.1', axis=1)

df = df.dropna(axis=0, subset=['ArrTime', 'ArrDelay', 'DepDelay', 'DepTime', 'ActualElapsedTime', 'CRSElapsedTime', 'Distance'])

# Datetime processing
dates = df.ix[:, ['Year', 'Month', 'DayofMonth']]
dates.columns = ['year', 'month', 'day']
dates = pd.to_datetime(dates, infer_datetime_format=True)
df['Date'] = dates

# Select flights leaving Seattle
df_origin_sea = df.ix[df['Origin'] == 'SEA', :]

# Alaska Airlines indicator
df_origin_sea['Alaska'] = (df_origin_sea['UniqueCarrier'] == 'AS').astype(int)

# Limit to after 2008-12-01 to eliminate runway effects
df_origin_sea_3rwy = df_origin_sea.ix[df_origin_sea['Date'] > '2008-12-01', :]

carrier_dummies = pd.get_dummies(df_origin_sea_3rwy.ix[:, ['UniqueCarrier']])

# Get model
df_model = pd.concat((df_origin_sea, carrier_dummies), axis=1, ignore_index=True)

# Test
print df_model.head(1).T
print df_model.info()

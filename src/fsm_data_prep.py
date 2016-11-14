import pandas as pd
import numpy as np

df = pd.read_csv('./data/sea_all_years.csv')

# Drop unnamed column and NA
df = df.drop('Unnamed: 0', axis=1)
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
df_origin_model = df_origin_sea.ix[df_origin_sea['Date'] > '2008-12-01', :]

# Get dummies
dummy_cols = ['UniqueCarrier', 'DayOfWeek', 'Month']

def concatenate_cols(df1, df2):
    return pd.concat((df1, df2), axis=1)

def dummify(df, cols):
    for c in cols:
        dummies = pd.get_dummies(df.ix[:, [c]])
        df = concatenate_cols(df, dummies)
    return df

# Make model dataframe
df_model = dummify(df_origin_model, dummy_cols)

# Create indicator / class / y values
df_model['Delay_15_Indicator'] = (df_model['DepDelay'] >= 15).astype(int)
y = df_model.pop('Delay_15_Indicator')

# Columns for first model.
cols_m1 =  ['AirTime',
            'CRSDepTime',
            'UniqueCarrier_AS',
            'UniqueCarrier_B6',
            'UniqueCarrier_CO',
            'UniqueCarrier_DL',
            'UniqueCarrier_F9',
            'UniqueCarrier_FL',
            'UniqueCarrier_HA',
            'UniqueCarrier_NK',
            'UniqueCarrier_NW',
            'UniqueCarrier_OO',
            'UniqueCarrier_UA',
            'UniqueCarrier_US',
            'UniqueCarrier_VX',
            'UniqueCarrier_WN',
            'DayOfWeek_2',
            'DayOfWeek_3',
            'DayOfWeek_4',
            'DayOfWeek_5',
            'DayOfWeek_6',
            'DayOfWeek_7',
            'Month_10', 'Month_11', 'Month_12',
            'Month_2', 'Month_3', 'Month_4'
            'Month_5', 'Month_6', 'Month_7',
            'Month_8', 'Month_9']

X = df_model.ix[:, np.in1d(df_model.columns.values, cols_m1)]

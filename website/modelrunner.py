import numpy as np
import pandas as pd
import statsmodels.api as sm
import cPickle as pickle
from datetime import date, datetime, timedelta
import holidays

airline_to_code = { 'American': 'AA',
                    'Alaska': 'AS',
                    'JetBlue': 'B6',
                    'Continental': 'CO',
                    'Delta': 'DL',
                    'Frontier': 'F9',
                    'AirTrain': 'FL',
                    'Hawaiian': 'HA',
                    'Northwest': 'NW',
                    'SkyWest': 'OO',
                    'United': 'UA',
                    'US': 'US',
                    'Virgin America': 'VX',
                    'Southwest': 'WN',
                    'Spirit': 'NK'}

def initialize():
    with open('static/datafiles/minus3_split_model.pkl', 'r') as f:
        split_model = pickle.load(f)
    pos_model = sm.regression.linear_model.RegressionResults.load('static/datafiles/gammlog_pos.pickle')
    neg_model = sm.regression.linear_model.RegressionResults.load('static/datafiles/gammlog_neg.pickle')
    return split_model, neg_model, pos_model

def prep_point(X_point):
    cols_for_df = ['const', 'AirTime', 'Year', 'CRSDepTime', 'lat', 'long',
                   'DepDelayr', 'AvgArrDelay', 'wint_hol_1day', 'wint_hol_2day',
                   'fri_bef_mon_holiday', 'DayOfWeek_2', 'DayOfWeek_3', 'DayOfWeek_4',
                   'DayOfWeek_5', 'DayOfWeek_6', 'DayOfWeek_7', 'Month_2', 'Month_3',
                   'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8', 'Month_9',
                   'Month_10', 'Month_11', 'Month_12', 'DayofMonth_2', 'DayofMonth_3',
                   'DayofMonth_4', 'DayofMonth_5', 'DayofMonth_6', 'DayofMonth_7',
                   'DayofMonth_8', 'DayofMonth_9', 'DayofMonth_10', 'DayofMonth_11',
                   'DayofMonth_12', 'DayofMonth_13', 'DayofMonth_14', 'DayofMonth_15',
                   'DayofMonth_16', 'DayofMonth_17', 'DayofMonth_18', 'DayofMonth_19',
                   'DayofMonth_20', 'DayofMonth_21', 'DayofMonth_22', 'DayofMonth_23',
                   'DayofMonth_24', 'DayofMonth_25', 'DayofMonth_26', 'DayofMonth_27',
                   'DayofMonth_28', 'DayofMonth_29', 'DayofMonth_30', 'DayofMonth_31']
    test_df = pd.DataFrame(columns=cols_for_df)
    for c in X_point.columns:
        test_df[c] = X_point[c]
    dummies = {'DayOfWeek_': int(X_point.DayOfWeek.values[0]),
                  'Month_': int(X_point.Month.values[0]),
                  'DayofMonth_': int(X_point.DayofMonth.values[0])}
    for k in dummies:
        if dummies[k] > 1:
            test_df.ix[X_point.index, [k+str(dummies[k])]] = 1
    test_df['const'] = [1]
    test_df = test_df.fillna(0)
    test_df = test_df.drop(['DayOfWeek', 'DayofMonth', 'Month'], axis=1)
    return test_df

def classifier_predict(raw_point, clf):
    probs = clf.predict_proba(raw_point)
    return probs

def pos_neg_predict(X_t, prob_right, mod_pos, mod_neg):

    gamm_log_results = mod_pos
    gamm_log_results_neg = mod_neg

    yhat_positive = gamm_log_results.predict(X_t)
    yhat_negative = gamm_log_results_neg.predict(X_t)

    binom_sample = np.random.binomial(1, prob_right, 100000)
    left_sample = np.random.exponential(yhat_negative, 100000)
    right_sample = np.random.exponential(yhat_positive, 100000)
    left_sample = (-left_sample) - 3
    right_sample = right_sample - 4
    samples = (binom_sample * right_sample) + ((1 - binom_sample) * left_sample)
    return samples

def transform_user_input(origin, dest, airline, year, month, day, time, lookupdf):
    '''
    Take raw info selected by user on form and transform into dataframe row
    ready for the models. Handles day of week and holidays, but time must be
    received as military format (e.g. 7:40pm = 1940)
    '''

    xdf = pd.DataFrame(columns=['AirTime', 'DayOfWeek', 'DayofMonth',
                                'Month', 'Year', 'CRSDepTime',
                                'lat', 'long', 'DepDelayr', 'AvgArrDelay',
                                'wint_hol_1day', 'wint_hol_2day',
                                'fri_bef_mon_holiday'])
    airline = airline_to_code[airline]
    relpoint = lookupdf.ix[(lookupdf['airport'] == dest) & (lookupdf['UniqueCarrier'] == airline), :]
    # Check to see if route/airline combo has never occured
    if len(relpoint) <= 0:
        return relpoint

    xdf['lat'] = relpoint['lat']
    xdf['long'] = relpoint['long']
    xdf['DepDelayr'] = relpoint['DepDelayr']
    xdf['AvgArrDelay'] = relpoint['AvgArrDelay']
    xdf['AirTime'] = relpoint['AirTime']
    xdf['Month'] = month
    xdf['DayofMonth'] = day
    xdf['Year'] = year
    xdf['CRSDepTime'] = time
    xdf = date_processing(xdf)
    return xdf

def date_processing(df_in):
    df_out = df_in
    df_out['Day'] = df_out['DayofMonth']
    df_out['Date'] = pd.to_datetime(df_in.ix[:, ['Year', 'Month', 'Day']], infer_datetime_format=True)
    df_out = holiday_checker(df_out)
    df_out['DayOfWeek'] = np.array(df_out.Date.astype(datetime))[0].isoweekday()
    df_out = df_out.drop(['Day', 'Date'], axis=1)
    return df_out

def holiday_checker(df_in):
    usholidays = holidays.UnitedStates()
    date = np.array(df_in.Date.astype(datetime))[0]
    plus3 = date + timedelta(days=3)
    plus2 = date + timedelta(days=2)
    plus1 = date + timedelta(days=1)
    # Friday before Monday holidays
    if ((plus3 in usholidays) & (plus3.isoweekday() == 1)):
        df_in['fri_bef_mon_holiday'] = 1
    else:
        df_in['fri_bef_mon_holiday'] = 0

    if ((plus2 in usholidays) & (plus2.day in range(22, 29)) & (plus2.month in range(11, 13))):
        df_in['wint_hol_2day'] = 1
    else:
        df_in['wint_hol_2day'] = 0

    if ((plus1 in usholidays) & (plus1.day in range(22, 29)) & (plus1.month in range(11, 13))):
        df_in['wint_hol_1day'] = 1
    else:
        df_in['wint_hol_1day'] = 0
    return df_in

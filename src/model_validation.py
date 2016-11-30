import pandas as pd
import numpy as np
import modelrunner as mr
import statsmodels.api as sm
from scipy.stats import percentileofscore
import cPickle as pickle

def initialize():
    with open('../website/static/datafiles/minus3_split_model.pkl', 'r') as f:
        split_model = pickle.load(f)
    pos_model = sm.regression.linear_model.RegressionResults.load('../website/static/datafiles/gammlog_pos.pickle')
    neg_model = sm.regression.linear_model.RegressionResults.load('../website/static/datafiles/gammlog_neg.pickle')
    return split_model, neg_model, pos_model

def test_value(df_row):
    origin = 'SEA'
    dest = df_row['Dest']
    airline = df_row['UniqueCarrier']
    year = df_row['Year']
    month = df_row['Month']
    day = df_row['DayofMonth']
    time = df_row['CRSDepTime']

    point = mr.transform_user_input(origin, dest, airline, year, month, day, time, lookupdf)
    probabilities = mr.classifier_predict(point, clf)
    dist_samples = mr.pos_neg_predict(mr.prep_point(point), probabilities[0][1], pos_model, neg_model)
    return (pd.Series(dist_samples).mean(), 100 - percentileofscore(dist_samples, 15, kind='strict'))


df = pd.read_csv('../data/final_validation/sep2016validation.csv')

df = df.ix[df['Origin'] == 'SEA', :]

print df.info()

df = df.drop('Unnamed: 0', axis=1)

df = df.dropna(axis=0, subset=['ArrTime', 'ArrDelay', 'DepDelay', 'DepTime',
                               'ActualElapsedTime', 'CRSElapsedTime',
                               'Distance'])

df = df.ix[(pd.isnull(df['WeatherDelay'])) |
                                (df['WeatherDelay'] == 0), :]

df = df.reset_index()

print df.info()

with open('../website/static/datafiles/lookupdf.pkl', 'r') as f:
    lookupdf = pickle.load(f)

clf, neg_model, pos_model = initialize()

predictions = []
probabilities = []



df.to_csv('validation_clean.csv')

# for i in range(0, len(df)):
#     if i % 100 == 0:
#         print(float(i) / len(df))
#     predictions.append(test_value(df.iloc[i, :])[0])
#     probabilities.append(test_value(df.iloc[i, :])[1])
#
#
# with open('sep2016_predictions.pkl', 'w') as f:
#     pickle.dump(predictions, f)
#
# with open('sep2016_probabilities.pkl', 'w') as f:
#     pickle.dump(probabilities, f)

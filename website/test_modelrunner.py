import modelrunner as mr
import pandas as pd
import numpy as np
import statsmodels.api as sm
import cPickle as pickle

origin = 'SEA'
dest = 'Albuquerque International'
airline = 'Southwest'
year = 2017
month = 12
day = 23
time = 834

clf, neg_model, pos_model = mr.initialize()

with open('static/datafiles/lookupdf.pkl', 'r') as f:
    lookupdf = pickle.load(f)

point = mr.transform_user_input(origin, dest, airline, year, month, day, time, lookupdf)
print point
print mr.classifier_predict(point, clf)
probabilities = mr.classifier_predict(point, clf)
dist_samples = mr.pos_neg_predict(mr.prep_point(point), probabilities[0][1], pos_model, neg_model)
print pd.Series(dist_samples).median()

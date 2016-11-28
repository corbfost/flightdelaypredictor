import numpy as np
import pandas as pd

def initialize():
    with open('static/datafiles/minus3_split_model.pkl', 'r') as f:
        split_model = pickle.load(f)
    with open('static/datafiles/neg_gammlog.pkl', 'r') as f:
        neg_model = pickle.load(f)
    with open('static/datafiles/pos_gammlog.pkl', 'r') as f:
        pos_model = pickle.load(f)
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
    X_point = pd.DataFrame(X_point).T
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

def classifier_predict(raw_point):
    probs = clf.predict_proba(raw_point)
    return probs

def pos_neg_predict(X_t, left_bound, right_bound, prob_right):

    yhat_positive = gamm_log_results.predict(X_t)
    yhat_negative = gamm_log_results_neg.predict(X_t)

    binom_sample = np.random.binomial(1, prob_right, 10000)
    left_sample = np.random.exponential(yhat_negative, 10000)
    right_sample = np.random.exponential(yhat_positive, 10000)
    left_sample = (-left_sample) - 3
    right_sample = right_sample - 4
    samples = (binom_sample * right_sample) + ((1 - binom_sample) * left_sample)
    return samples

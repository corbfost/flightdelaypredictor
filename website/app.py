import os
from flask import Flask, render_template, jsonify, request
import random_data
import modelrunner as mr
import pandas as pd
import numpy as np
import cPickle as pickle
from sklearn.ensemble import GradientBoostingClassifier
from scipy.stats import percentileofscore
from datetime import datetime

app = Flask(__name__)

airline_codes = {'AA': 'American',
                 'AS': 'Alaska',
                 'B6': 'JetBlue',
                 'CO': 'Continental',
                 'DL': 'Delta',
                 'F9': 'Frontier',
                 'FL': 'AirTran',
                 'HA': 'Hawaiian',
                 'NW': 'Northwest',
                 'OO': 'SkyWest',
                 'UA': 'United',
                 'US': 'US',
                 'VX': 'Virgin America',
                 'WN': 'Southwest',
                 'NK': 'Spirit'}

def converttime(timestamp):
    timestamp = timestamp.astype(str)
    ts = timestamp.split('.')
    ts = ts[0]
    if len(ts) < 4:
        hour = ts[0]
        minutes = ts[1:]
        ampm = ' am'
    else:
        hour = int(ts[0:2])
        minutes = ts[2:]
        ampm = ' pm'
        if hour >= 13:
            hour = hour - 12
    return str(hour) + ':' + minutes + ampm

def initialize_model():
    with open('static/datafiles/model.pkl', 'r') as f:
        model = pickle.load(f)
    with open('static/datafiles/airport_names.pkl', 'r') as f:
        airport_names = pickle.load(f)
    return model, airport_names

def run_model(df, mod):
    X = df.ix[:,
              ['AirTime',
               'DayOfWeek', 'DayofMonth', 'CRSDepTime',
               'Distance', 'Month', 'Year', 'Alaska',
               'AvgArrDelay']].values
    prediction = mod.predict_proba(X)
    return prediction

def pred_parse(p):
    p_text = str(round(p, 4) * 100) + "%"
    if p >= .13:
        return "delayed", p_text
    else:
        return "on-time", p_text

def parse_delay(samples):
    median = round(pd.Series(samples).mean(), 1)
    if median < 0:
        return str(abs(median)) + ' minutes early'
    elif median == 0:
        return 'Exactly on time!'
    else:
        return str(median) + ' minutes late'

def find_intensity(probability):
    if probability < 7:
        return "low"
    elif probability < 17:
        return "moderate"
    else:
        return "severe"

@app.route("/")
def index():
    return render_template('index.html', title='Flight Delays')

# @app.route("/_get_data")
# def data_sample():
#     # Get random sample from data
#     data = random_data.grab_sample()
#
#     # Get prediction from data
#     prediction, perc = pred_parse(run_model(data, model)[:, 1][0])
#
#     data = data.to_dict(orient='list')
#     airline = data['UniqueCarrier'][0]
#     dt = (data['Date'][0]).strftime('%A, %B %d, %Y')
#     tm = converttime(data['CRSDepTime'][0])
#     actual = data['DepDelay'][0]
#     dest = data['Dest'][0]
#     return jsonify(airline=airline_codes[airline],
#                    date=dt,
#                    time=tm,
#                    actual=actual,
#                    dest=airport_names[dest],
#                    pred=prediction,
#                    percentage=perc)

@app.route("/result")
def result():
    origin = request.args.get('origin', 0, type=str)
    dest = request.args.get('dest', 0, type=str)
    airline = request.args.get('airline', 0, type=str)
    year = request.args.get('year', 0, type=int)
    month = request.args.get('month', 0, type=int)
    day = request.args.get('dayofmonth', 0, type=int)
    time = int(request.args.get('hour', 0, type=str) +
               request.args.get('minutes', 0, type=str))
    print(dest + 'b')
    point = mr.transform_user_input(origin, dest, airline, year, month, day, time, lookupdf)

    # Handle route does not exist error
    if len(point) <= 0:
        return jsonify(result="Data not available", percentile="", intensity='severe')
    else:
        probabilities = mr.classifier_predict(point, clf)
        dist_samples = mr.pos_neg_predict(mr.prep_point(point), probabilities[0][1], pos_model, neg_model)
        predicted_delay = parse_delay(dist_samples)
        prob15 = round(100 - percentileofscore(dist_samples, 15, kind='strict'), 2)
        intensity = find_intensity(prob15)
    return jsonify(result=predicted_delay, likelihood=prob15, intensity=intensity)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == "__main__":

    clf, neg_model, pos_model = mr.initialize()
    with open('static/datafiles/lookupdf.pkl', 'r') as f:
        lookupdf = pickle.load(f)

    app.run(host='0.0.0.0', port=8080, debug=True)

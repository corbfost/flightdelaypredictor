import os
from flask import Flask, render_template, jsonify, request
import random_data
import pandas as pd
import numpy as np
import cPickle as pickle
from sklearn.ensemble import GradientBoostingClassifier
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
                 'WN': 'Southwest'}

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
    with open('../data/model.pkl', 'r') as f:
        model = pickle.load(f)
    with open('../data/airport_names.pkl', 'r') as f:
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

@app.route("/")
def index():
    return render_template('index.html', title='Test !')

@app.route("/_get_data")
def data_sample():
    # Get random sample from data
    data = random_data.grab_sample()

    # Get prediction from data
    prediction, perc = pred_parse(run_model(data, model)[:, 1][0])

    data = data.to_dict(orient='list')
    airline = data['UniqueCarrier'][0]
    dt = (data['Date'][0]).strftime('%A, %B %d, %Y')
    tm = converttime(data['CRSDepTime'][0])
    actual = data['DepDelay'][0]
    dest = data['Dest'][0]
    return jsonify(airline=airline_codes[airline],
                   date=dt,
                   time=tm,
                   actual=actual,
                   dest=airport_names[dest],
                   pred=prediction,
                   percentage=perc)

if __name__ == "__main__":
    model, airport_names = initialize_model()
    app.run(host='0.0.0.0', port=8080, debug=True)

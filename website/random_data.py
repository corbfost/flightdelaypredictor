import pandas as pd
import cPickle as pickle
from flask import jsonify

def grab_sample():
    with open('../data/modeldata.pkl', 'r') as f:
        df = pickle.load(f)
        sample = df.sample(n=1, replace=True)
        return sample

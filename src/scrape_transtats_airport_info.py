import requests
import pandas as pd
import numpy as np
import cPickle as pickle
from bs4 import BeautifulSoup

url = "http://www.transtats.bts.gov/airports.asp?pn=1&Airport="

with open('../data/airports.pkl', 'r') as f:
    airports = pickle.load(f)

df = pd.DataFrame([['_',0, 0, 0]], columns=['Airport', 'Year', 'AvgDepDelay', 'AvgArrDelay'])
years = [2011, 2012, 2013, 2014, 2015, 2016]
Departure_delays = []
Arrival_delays = []
Airport_lst = []
Year_lst = []

for a in airports:
    print "Retrieving data for: ", a
    r = requests.get(url + a)
    b = BeautifulSoup(r.content, 'lxml')

    t = b.find_all("td")
    txts = [i.text for i in t]
    try:
        start = txts.index("Avg Delay (min.)")
        end = txts.index("% Cancelled")
    except:
        continue

    rel = [i for i in txts[start:end]]

    Departure_delays = Departure_delays + [float(d) for d in rel[2:8]]
    Arrival_delays = Arrival_delays + [float(ar) for ar in rel[10:16]]
    Airport_lst = Airport_lst + [a for n in years]
    Year_lst = Year_lst + [n for n in years]


df = df.append([pd.Series(Departure_delays), pd.Series(Arrival_delays),
               pd.Series(Airport_lst), pd.Series(Year_lst)], ignore_index=True)

df = df.T.drop(0, axis=1).reset_index().drop('index', axis=1).dropna()
df.columns = ['AvgDepDelay', 'AvgArrDelay', 'Airport', 'Delay_Yr']

with open('airport_info.pkl', 'w') as f_:
    pickle.dump(df, f_)

# Pull in aggregate CSV data, limit to Seattle, and save in new folder as CSV.

import pandas as pd

nums = range(1988, 2009)

def read_select_seatac(year_range):
    for n in year_range:
        print "Reading CSV for {}".format(n)
        df = pd.read_csv('data/87_08_data/' + str(n) + '.csv.bz2', compression='bz2')
        df = df.ix[(df['Origin'] == 'SEA') | (df['Dest'] == 'SEA'), :]
        print "Writing the limited CSV"
        df.to_csv('./data/sea_limited_data/' + str(n) + '.csv')
    return "Success!"

print read_select_seatac(nums)

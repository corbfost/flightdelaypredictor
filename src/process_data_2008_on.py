import pandas as pd
import zipfile
import fnmatch
import os

dir_name = '/Users/cf/Documents/Galvanize/flight_delays/data/final_validation'
extension = ".zip"

os.chdir(dir_name)

print "Extracting ... "
for i, item in enumerate(os.listdir(dir_name)):
    # loop through items in dir
    print "{}% done".format(round(float(i)/len(os.listdir(dir_name)), 2)*100)
    # check for ".zip" extension
    if item.endswith(extension):
        file_name = os.path.abspath(item)  # get full path of files
        zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
        zip_ref.extractall(dir_name + '/unzipped_csvs/')  # extract file to dir
        zip_ref.close()  # close file

print "Success!"

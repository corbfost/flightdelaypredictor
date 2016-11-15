
#### First look at compiled data ####

- 5,578,482 rows (flights)
- Check missing values:
  For each column, percentage of them that aren't null:
      ActualElapsedTime 0.986472126288
      AirTime 0.800813375395
      ArrDelay 0.986472126288
      ArrTime 0.986957204487
      CRSArrTime 1.0
      CRSDepTime 1.0
      CRSElapsedTime 0.999932239631
      CancellationCode 0.0036784200433
      Cancelled 1.0
      CarrierDelay 0.231469600511
      DayOfWeek 1.0
      DayofMonth 1.0
      DepDelay 0.988878157176
      DepTime 0.988878157176
      Dest 1.0
      Distance 0.997221824862
      Diverted 1.0
      FlightNum 1.0
      LateAircraftDelay 0.231469600511
      Month 1.0
      NASDelay 0.231469600511
      Origin 1.0
      SecurityDelay 0.231469600511
      TailNum 0.811498898804
      TaxiIn 0.810032729334
      TaxiOut 0.810203205818
      UniqueCarrier 1.0
      WeatherDelay 0.231469600511
      Year 1.0

- What can we see here...
  - Date information is complete
  - Carrier info is complete
  - Delay type only exists for flights with delays (makes sense)
  - Distance not quite complete (but close)
  - Arrival and Dep Delay at almost 98% - good.

  - Dropping the nulls for columns that were close to 100 complete
  takes out 90,766 flights, which is only 1.6%
  - The mean departure delay is ever so slightly lower without the dropped flights.
  - Same with arrival delay. Should not be large enough to matter.

- Just realized that dates are not stored anywhere as datetime.
  -  Attempting to convert them is taking forever so far, unfortunately.
  - Attempting to save converted as another CSV - we'll see how large it gets.
  - Wasn't pretty, but got dates working smoothly now by merging dataframes. Total file is not big enough to be unworkable in Pandas.


## EDA:

- Delays by date.
- Highly erratic overall - lots of noise.
- Outliers:
  - January 18-19th, 2012 = Major Snow/Ice Storm
  - Other ice storms and snow storms

- Date effects:
  - Months: Delays significantly worse June-August (Summer spike)
  - Day of Week: Thursday and Friday are significantly worse, consistently
  throughout the year
  - November looking interesting - Day of week effects seem to flip, with Monday and Sunday suddenly looking worse. Interesting.
  - Holidays:

- Carriers:
  - Looking at distribution through time, Alaska's complete dominance becomes
  apparent.
  - Besides Alaska, these airlines are blips on the chart:
    American, Delta, SkyWest, United, and Southwest

  - Most fascinating finding yet: Average delay for Alaska flights has dipped consistently below all other airlines since about ~2009. Significantly and VERY consistently below.
    - Possible reason: Opening of 3rd runway in Nov. 2008.
    - Really fascinating though that this new runway only helped Alaska's delays.

#### Model considerations from EDA:
- Limit year selection to after the 3rd runway was installed.
- Code day of week, month, into dummies.
- Include year.
- Include carrier dummy
- Include interactions between day of week and Months(?)
- Ignore (perhaps) weather delays
- Manually classify delays as >15 minutes.

#### First shitty model
- Included 'AirTime', 'CRSDepTime', carrier dummies, day of week dummies, month dummies.
- Fit 70% of data to sklearn Logistic Regression model using built-in class weighting
- Performance:
  - Accuracy: .61
  - Recall: .58
  - Precision: .19

- Notes:
  - Low accuracy is not the end of the world - mainly because of the recall. 58%
  recall is pretty good, according to industry standards which shoot for 60%.
  This means that of all the true delays, the model captured 60%. The cost though
  is revealed in the low precision. It is over-predicting the minority class, meaning
  only 19% of it's predicted positives are truly positive.

  - It would now be extremely interesting to link a regression-type predictor
  to the data, mainly because we could see if low prediction %'s are linked to smaller delays.
  I could also create a custom cost function that minimizes the number of predicted positives
  scaled by the magnitude of the predicted delay.

#### Further EDA, feature engineering.

- Created a 'business' variable to measure how many flights are departing in a given 10 min time interval.
  - It didn't perform particularly well. In fact, the greater the business, the lower the delays seemed to get. Even looking at lagged delays (number of flights scheduled in 10 min blocks at increasing lags behind current flight) didn't reveal much.

#### Gradient Boosted Classifier and Regressor:

- Limited delays to only flights not delayed by weather.
- Fit a gradient boosted classifier on the following columns:
```
 'AirTime', 'ArrTime',
 'DayOfWeek', 'DayofMonth', 'DepTime',
 'Distance',
 'Month',  
 'Year', 'Alaska',
 'business_indicator',
 'business_indicator_lagged_1', 'business_indicator_lagged_2',
 'business_indicator_lagged_3', 'business_indicator_lagged_4',
 'business_indicator_lagged_5', 'business_indicator_lagged_6',
 'business_indicator_lagged_7', 'business_indicator_lagged_8',
 'business_indicator_lagged_9', 'business_indicator_lagged_10',
 'business_indicator_lagged_11', 'business_indicator_lagged_12'
```
- 'Alaska' is an indicator variable for Alaska airlines (1 = Alaska, 0 = other airline).
- Metrics:
```
Accuracy:  0.875834302916
Recall:  0.0903964265773
Precision:  0.757958801498
```
- Ok, so horrible recall. But the ROC curve suggests that adjusting the threshold will help. Setting the threshold to .13 gives the following scores:
```
Accuracy:  0.681371082424
Recall:  0.720212171971
Precision:  0.252822422579
```
- Not bad at all, actually. Both precision and recall are significantly higher compared to the Logistic model. 

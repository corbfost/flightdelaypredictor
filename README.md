# Flight Delay Predictor
### A new approach to predicting flight delays using machine learning.
#### Data Source:
Bureau of Transportation Statistics On-Time Performance Data
#### Model:

*Theoretical considerations:*
At a basic level, flight delays are not normally distributed; early departures are limited by natural constraints, whereas late departures are boundless. In my dataset, actual departures ranged from 54 minutes early to 1,964 minutes late (yikes!), with a median value of 2 minutes early. If we consider early departures to be negative delays, you can visualize the distribution.

[INSERT IMAGE HERE]

In the graph above, we can see that flights almost never leave more than 15 minutes early, but leave 15 minutes late fairly often (roughly 15% of the time, to be exact). If the data were normally distributed, we'd expect the distribution to look the same on both sides of the median. But it does not. This breaks assumptions inherent in fitting a cookie-cutter OLS regression to the data.

Clearly a custom-made, creative solution is necessary to make headway with this problem. From a statistical standpoint, if you were to split the data at -2, you can visualize the data as falling into two exponential distributions: one extending from -2 to infinity, and one extending from -2 to negative infinity.

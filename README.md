# A Study on Predicting Property Values

Betterview is an Insurtech company that created a platform for generating and analyzing roofs of properties at cost/scale that was impossible until recently. Imagery of cities is captured on a regular basis by manned aircraft and stiched into a large orthomap with 7 cm resolution (compared to the typical 30 cm resolution and often many years old imagery of Google Maps). Check out the provider of this imagery, Nearmap, to learn more about this. Betterview's platform combines image classification with human labeling to derive data on the condition of roofs based on addresses provided by their clients (primarily insurance companies.

## Example of Imagery from Nearmap
![](/images/nearmap_example.png)

## Example of Imagery from Google Maps
![](/images/google_example.png)

## Modeling a Score to Summarize the Roof Data
Based on the data derived from this imagery, Betterview has created a model to quantify this data in terms of its bearing on property insurance risk. This score has shown to be a valuable tool in separating good risks from bad risks. 

## Why Real Estate?
If you know many people who have bought a house (will most likely have to think outside of the Bay Area for this), you have likely heard about negotiating processes. And specifically one item that comes up frequently in these negotiating processes is the condition of the roof. It can cause deals to fall through or sellers to concede on price if it not in good shape.

It would stand to reason that many of the same factors that contribute to a roof being a bad insurance risk (having existing damage, wear, etc) may also contribute to having less value on the real estate market. To test this theory, we need data.

# The Study
Given approximately 85,000 locations with roof data from Betterview over the last year, we need to be able to pair that data with the property value estimate that matches its date. This should be feasible for any property that will show up in a search of a real estate website. However, getting this matching property value estimate is meaningless if we don't have a record of a sale after the fact as a target upon which to train (or validate as the case may be). Given that our access to sales data is better than our access to historical property value estimates (API vs scraping real estate sites), it is prudent to first narrow down our list of candidate properties for the study to those that have sold after Betterview's data was generated.

Data Pipeline
1. SQL Query to Betterview and output as CSV.
2. Run the CSV through a master script that hits the Attom API and outputs a new CSV with relevant sales data appended as new columns.
3. With the same master script, take all properties with relevant sales data and scrape Realtor.com for the pertinent historical value estimate.

The above pipeline was decided upon after much trial and error with Zillow API and scraping. Through this exploratory phase, it was learned that Selenium could be a valuable tool that would still yield value in scalable scraping of Realtor.com. Although this data has yet to be gathered for the whole of our initial sample, the concepts have been proven. 

With the limits of Attom's 30 free trial including a 4000 hit/day limit, it will take about 20 days to cover all of these properties. 

### Selenium In Action
![](/images/selenium_demo.gif)

# The Data:
* Betterview: Categorical roof features (such as existing damage, patching, ponding, etc) and visual score

The Visual Scores for the ~85,000 properties appears to be exponentially distributed:

![](/images/visual_score_hist.png)

And again but with a log scale on the Y Axis:

![](/images/visual_score_hist_log.png)

# Hypothesis
As alluded to previously, the theory is that when a property has a lower Visual Score due to problems with its roof, this will correlate to selling prices that are lower than expected. 

Stated mathematically:

Where 	E = realtor estimate
		V = visual score
		S = sales price
        82 = mean of visual scores for this sample
        
             (S - E)/STD(S's)   -   (V - MEAN(V's))/STDEV(V's)      =    0 

Testing of this hypothesis would be performed using Welch's t Test for comparing two samples.




# A Study on Predicting Property Values

Betterview is an Insurtech company that created a platform for generating and analyzing roofs of properties at cost/scale that was impossible until recently. Imagery of cities is captured on a regular basis by manned aircraft and stiched into a large orthomap with 7 cm resolution (compared to the typical 30 cm resolution and often many years old imagery of Google Maps). Check out the provider of this imagery, Nearmap, to learn more about this. Betterview's platform combines image classification with human labeling to derive data on the condition of roofs based on addresses provided by their clients (primarily insurance companies.

### Example of Imagery from Nearmap
![](/images/nearmap_example.png)

### Example of Imagery from Google Maps
![](/images/google_example.png)

### Modeling a Score to Summarize the Roof Data
Based on the data derived from this imagery, Betterview has created a model to quantify this data in terms of its bearing on property insurance risk. This score has shown to be a valuable tool in separating good risks from bad risks. 

### Why Real Estate?
If you know many people who have bought a house (most likely need to think outside of the Bay Area for this), you have likely heard about the negotiations associated with purchasing property. And specifically one item that comes up frequently in these negotiations is the condition of the roof. It can cause deals to fall through or sellers to make large concessions on price if it not in good shape.

Naturally, it would stand to reason that many of the same factors that contribute to a roof being a bad insurance risk (having existing damage, wear, etc) may also contribute to having less value on the real estate market. To test this theory, we need data.

# The Study

Given Betterview's roof data and visual scores for approximately 85,000 locations from over the last year, records of sales after the time such data was generated, and property value estimates from the same time that the data was generated, one could determine the viability of using this roof data in estimating selling price. 

Given that our access to sales data is much better than our access to historical property value estimates (API vs scraping real estate sites), it is prudent to first narrow down our list of candidate properties for the study to those that have sold after Betterview's data was generated. This is expected to yield about a 1% return rate (or perhaps lower) for which our actual study can be conducted.

Data Pipeline
1. SQL Query to Betterview and output as CSV.
2. Run the CSV through a master Python script that hits the Attom API and outputs a new CSV with relevant sales data appended as new columns.
3. With the same master script, take all properties with relevant sales data and scrape Realtor.com for the pertinent historical value estimate.

### David vs Zilliath
The above pipeline was decided upon after much trial and error with Zillow API and scraping. Zillow's API does not allow for caching or storing of their data, and if a user makes more than 1,000 calls in a day, their access is shut off until Zillow can review their usage to ensure it qualifies with the Terms and Conditions. Further, Zillow's API for historical data is limited to an image of a graph of historical value estimates, and making matters worse, this image is not explicitly provided, but rather a URL is given where an image is simply displayed (and the image file's source cannot be extracted from the HTML). Retrieving historical values from this graph would be feasible with automated screen grabs and image processing; however, that would not fit within the timelines/scope of this project. 

Zillow does provide detailed data on their historical value estimate graph in their UI; however, it is only seen in the HTML after a dropdown is clicked and additional HTML is rendered via Javascript. This data was sought via scraping using Selenium and Beautiful Soup to navigate to the dropdown and click it; however, Beautiful Soup only retrieves the HTML from the page_source which is not updated upon clicking the dropdown. The possibility of using Scrapy and Splash was explored to retrieve the data after rendering through Selenium; however, Zillow's anti-bot systems immediately identified the use of Splash and would not cooperate.

It is also worth noting that numerous Captchas were completed even while going through test-sized samples of pages from Zillow with Selenium. Although, with more sophisticated cursor gestures and cookie management, perhaps this could be overcome. 

![](/images/captcha.png)

![](/images/terminator.png)


### Yet Hope Remains
Let us consider the old addage that when running from a bear, you don't have to run faster than the bear, you just have to run faster than the person next to you. While normally we consider this from the faster person's point of view, let us walk a mile in the shoes of the bear...

Well, just when this bear was getting pretty worn out chasing Zillow (although without enough time/resources still wants to catch it), it caught a glimpse of Realtor.com slowly plodding along. 

Yada yada yada...through exploratory phase, it was learned that Selenium could be a valuable tool that would still yield value in scalable scraping of Realtor.com. Although this data has yet to be gathered for the whole of our initial sample, the concepts have been substantiated (Realtor has been caught on numerous practice hunts).

### Selenium In Action
![](/images/selenium_demo.gif)

# The Data:

* Source Betterview: Categorical roof features (such as existing damage, patching, ponding, etc) and visual score for about 85,000 properties
* Source Attom API: Sales History for all properties - This data is still being obtained (will add some visuals/analysis if I can finish this document in time). With the limits of Attom's 30-day free trial including a 4000 hit/day limit, it will take about 20 days to cover all of these properties which is viable. 
* Source Realtor.com: Historical value estimates scraped from web. Estimating this will be performed on approximately 400 to 800 properties. Since we need historical estimates and not today's estimate, we mustAt about 20 seconds per page this would take about 5 hours (if all goes well). 

The Visual Scores for this sample appear to be exponentially distributed:

![](/images/visual_score_hist.png)

And again but with a log scale on the Y Axis:

![](/images/visual_score_hist_log.png)

# Hypothesis
As alluded to previously, the theory is that when a property has a lower Visual Score due to problems with its roof, this will correlate to selling prices that are lower than expected. The preliminary hypothesis could be summarized mathematically as follows:

Where:
E = realtor estimate
V = visual score
S = sales price
        
             (S - E)/STD(S's)   -   (V - MEAN(V's))/STDEV(V's)      =    0 

Testing of this hypothesis would be performed using Welch's t Test for comparing two samples.

Further development of this hypothesis and refinement of testing method is considered a likely need. Assistance of peers and industry professionals will be sought.

# Present Position and Proposed Action
Although collecting data has proven difficult and slow, the study appears to be viable for the time being. The pipeline for obtaining sales data has been established. The concept for scraping Realtor.com has been proven, although the consequences of scaling this up remain to be seen. 

This data scientist recommends continuing with the study.


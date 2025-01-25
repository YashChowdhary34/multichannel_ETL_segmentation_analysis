# Automated ETL with Predictive Customer Scoring & Lifetime Value Analysis

## Introduction

In the rapidly evolving business landscape understanding and predicting customer value has become paramount for organizations seeking to optimize their strategic decision-making.
This project focuses on Extract, Transform, Load (ETL) pipeline designed to transform raw retail sales data into actionable insights through sophisticated Customer Lifetime Value (CLV) prediction and comprehensive customer scoring mechanism.

## Overview

---

## Table of Contents

- [Dataset Overview](#dataset-overview)
- [Data Cleaning and Preprocessing](#data-cleaning-and-preprocessing)
- [Feature Engineering](#feature-engineering)
- [Splitting Outliers](#splitting-outliers)
- [Segmentation](#customer-segmentation)
- [Outlier Analysis](#outlier-analysis)
- [Segment Analysis](#segment-analysis)
- [Customer Lifetime Value Prediction](#)
- [Customer Churn Probability Prediction](#)
- [Predictive Customer Scoring](#)
- [ETL](#)
- [Findings](#)
- [Answering Business Problems](#)
- [Conclusion](#)

---

## Dataset Overview

The dataset that we are working with is collected from [UC Irvine Machine Learning Repository](#https://archive.ics.uci.edu/dataset/502/online+retail+ii). This Online Retail dataset contains all the transactions occurring for a UK-based and registered, non-store online retail between 01/12/2009 and 09/12/2011.The company mainly sells unique all-occasion gift-ware. Many customers of the company are wholesalers.

**Number of entries (tuples)** -> 525,461

**Features:**

- Invoice
- StockCode
- Description
- Quantity
- InvoiceDate
- Price
- Customer ID
- Country

---

## Data Cleaning and Preprocessing

**While exploring the dataset I came up with these following conclusions:**

1. Some entries have negative quantity and/or price values in them.
2. Description and CustomerID field have a bunch of missing values in them.
3. A valid Invoice number would be a 6-digit unique number, if the number starts with 'C' it indicates cancellation. One thing to note is, there are a bunch of numbers starting with 'A' which are bad debt adjustments.
4. Talking about StockCode, we have them as a 5-digit unique number followed by a character. But, I found 55 StockCodes (14 types) that are different from the said valid format. So, I went on and explored each one of them and found out that 'PADS' is the only value other than the conventional 5-digit letter code that seemed valid.
5. Some products where give out for free so their price values where set to 0.

**Actions that I took based on my finding:**

1. Removed entries that had negative quantity and/or price values in them.
2. Dropped all the tuples that had Invoice number other than a 6-digit unique number. This includes the cancelled orders and bad debth adjustment entries.
3. All the entires which didn't have a Customer ID in them where removed.
4. Removed entries that had SockCode values other than the 6-digit number followed by a character or 'PADS'.
5. Dropped tuples which had Price values set to 0 or where given out for free.

**Before Cleaning Dataset Size:** 4,203,688
**After Cleaning Dataset Size:** 3,250,472
**Percentage of data left:** 77.32%

---

## Feature Engineering

**There are 2 types of feature that we are going to be working with:**

- TimeSeries Features
- Customer Metrics Features

1. **TimeSeries Features**

Here is a list of features that I engineered for timeseries analysis and forecasing:

- TotalAmount
- Year
- Month
- DayOfWeek
- HourOfDay
- TimeOfDay

2. **Customer Metrics Features**

Here is a list of features that I engineered for segmentation and customer metrics analysis:

- TotalSpent
- Recency
- Frequency
- FirstInvoiceDate
- LastInvoiceDate
- CustomerLifespan

---

## Splitting Outliers

While segmenting the customers into multiple clusters/groups we are going to look at these following features (RFM):

- **Recency** - number of days it has been since the customer last purchased from the organization.
- **PurchaseFrequency** - how frequently does the customer buys or makes a purchase from the organization.
- **TotalSpent** - the monetary value that the customer brings to the organization.

**Here we have a box plot that shows the feature(RFM) distribution.**
// feature distribution box plot goes here //

**A brief overview of how to interpret the box-plot**
The box represents the 25th, 50th, 75th percentile of our data. The first line or the starting line of the box is the 25th percentile, the line in the middle is the median or 50th percentile and finally the topmost line or the line were the box ends is the 75th percentile. These percentiles basically represent the spread of the data. Finally the lines outside the box on the top and the bottom are essentially the interquartile range and the points of customers that are outside these lines or range are outliers.

**How and why do we need to split the outliers**
Splitting outliers in our data is important for further analysis, segmentation and increasing our model performance. Talking about how we are going to do it, we'll remove all the entries or tuples that lie outside the interquartile range or the top and bottom lines outside our box in the box-plot.

**Important thing to note** - we can't just drop the outliers as they represent the most valuable (high value, high frequency) customers of the organization. What we are going to do is split them and do a seperate analysis on the outliers.

**Here's the box plot that shows the feature(RFM) distribution after removing outliers**
// distribution after split goes here//

---

## Customer Segmentation

Customer Segmentation is crutial to understand the customers and their buying pattern, also gives the organization the benifit to deploy tailored marketing or sales strategies according to the customer segments/groups. This has a direct impact on the organizations performance and revenue.

**Steps to identify the valid number of segments/clusters:**

- Scaling the features are necessary to ensure that each feature has equal weightage
  I'll be using the StandarScaler that comes with scikit-learn preprocessing library to scale our RFM features.

- Clustering the data in the range of 2-10
  We'll group the data points into clusters, these clusters can be thought of as groups or segments of customers that share some similarity. I'll be using KMeans algorithm to cluster/segment our customers.

- To find out optimal number of clusters/segments we are going to be be looking at the inertia and silhouette score for each cluster number
  Inertia basically represents the distance betweeen each point/value and the center/centroid of the cluster, therefore we should target for a lower value of inertia. One thing to note here it as we increase the number of clusters/segments the inertia will drop up until each point/value becomes a segment itself, so we are going to be finding the elbow in the elbow curve to get the optimal value which isn't necessary the lowest value of inertia.
  Talking about silhouette score it's a score that represents the amount of overlap between each cluster/segment it's good to have a higher score which essentially translates to less overlap.

**Here we have a plot that shows the Elbow Curve and Silhouette Score for our features**
// line plot goes here //

**Optimal Cluster Analysis**

- We'll look for the "elbow" in the elbow curve and it's at 4 clusters, also the curve kind of plateaus after 5 clusters.
- Silhouette Score sharply decreases after 5 clusters and there isn't a big difference betweeen 4 and 5 cluster numbers.

**Number of Optimal Customer Segments -** 4

**Why not fewer Segments ?**
Cluster number 2 or 3 would merge critical segments and oversimplify our segments by grouping high/low spenders without nuance.

**Why not more Segments ?**
Cluster number 5 would likely split natural groups into artificial micro-segments. Also important thing to note here is that business goals prioritize simplicity over granularity.

---

## Outlier Analysis

**Understanding the Outliers**
Before performing any kind of analysis on our outliers first it's important to understand which customers do they represent. Broadly speaking they are the most valuable customers of the organization. They represent - the customers that produce the highest monetary value, the customers that purchase more frequently and are the most recent.

**Segmenting Outliers**
It's crutial to segment our outliers so that we can understand them better and develop tailored marketing and/or sales strategies.

Here's how we are going to segment them -

1. High Value Customers Only - Monetary Outliers
2. High Frequency Customers Only - Frequency Outliers
3. igh Value & High Frequency Customers - Monetary & Frequency Outliers (Whales)

**Let's look at the RFM Feature Spread so that we can come up with Segment Labels**
//violin plot goes here//

**Understanding Segment Labels**
We are going to assign action based labels so that we can easily identify the characteristics and strategy that we need to deploy for that particular customer.

1. **PAMPER** - Label (-1)
   **Characteristics** - High spenders but not necessarily frequent buyers. Their purchases are large but infrequent.
   **Strategy** - Focus on maintaining their loyalty with personalized offers or luxury services that cater to their high spending capacity.

2. **UPSELL** - Label (-2)
   **Characteristics** - Frequent buyers who spend less per purchase. These customers are consistently engaged but might benefit from upselling opportunities.
   **Strategy** - Implement loyalty programs or bundle deals to encourage higher spending per visit, given their frequent engagement.

3. **DELIGHT** - Label (-3)
   **Characteristics** - The most valuable outliers, with extreme spending and frequent purchases. They are likely your top-tier customers who require special attention.
   **Strategy** - Develop VIP programs or exclusive offers to maintain their loyalty and encourage continued engagement.

---

## Segment Analysis

As we have already segmented our customers into 4 clusters based on RFM features in the [Customer Segmentation](#customer-segmentation) step, now it's finally time to analyse the segments and come up with labels for our segments.

**First let's look at the 3-D scatter plot of customer data with different colors for each segments**

// scatter plot goes here //

**Now let's take a look at the segment spread for each feature(RFM)**

//violin plot goes here //

**Let's engineer some feature deepen our understanding of each segment**

//table goes here//

**Finally let's assing the segment labels and understand what each label really means**

1. Cluster 0 (Blue): "Retain"

- **Rationale:** This cluster represents high-value customers who purchase regularly, though not always very recently. The focus should be on retention efforts to maintain their loyalty and spending levels.
- **Action:** Implement loyalty programs, personalized offers, and regular engagement to ensure they remain active.

2. Cluster 1 (Orange): "Re-Engage"

- **Rationale:** This group includes lower-value, infrequent buyers who haven’t purchased recently. The focus should be on re-engagement to bring them back into active purchasing behavior.
- **Action:** Use targeted marketing campaigns, special discounts, or reminders to encourage them to return and purchase again.

3. Cluster 2 (Green): "Nurture"

- **Rationale:** This cluster represents the least active and lowest-value customers, but they have made recent purchases. These customers may be new or need nurturing to increase their engagement and spending.
- **Action:** Focus on building relationships, providing excellent customer service, and offering incentives to encourage more frequent purchases.

4. Cluster 3 (Red): "Reward"

- **Rationale:** This cluster includes high-value, very frequent buyers, many of whom are still actively purchasing. They are your most loyal customers, and rewarding their loyalty is key to maintaining their engagement.
- **Action:** Implement a robust loyalty program, provide exclusive offers, and recognize their loyalty to keep them engaged and satisfied.

**Summary of Cluster Names:**

- Cluster 0 (Blue): "Retain"
- Cluster 1 (Orange): "Re-Engage"
- Cluster 2 (Green): "Nurture"
- Cluster 3 (Red): "Reward"

---

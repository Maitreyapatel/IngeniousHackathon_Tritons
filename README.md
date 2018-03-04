# IngeniousHackathon_Tritons #

__Aim__: To build a category predictor. Classify the text description into pre-defined categories.

__Application__: Categorize government tendors' ads(descriptions) into CPV's of goods. CPV's are codes assigned to goods by European Union. The CPV establishes a single classification system for public procurement aimed at standardising the references used by contracting authorities and entities to describe the subject of procurement contracts. [More about CPV](https://simap.ted.europa.eu/cpv)

This will be helpful for categorizing government tendors into different product categories which presently,is performed manually.

## Approach:
Given a description, we will first find the product which describes it. Then find the assigned CPV of that product.


## Step 1: Setting the Design Philosophy of a categoriser:
Find the probability of categories which the description belongs to. 

In order to classify on the basis of probability, we have two methods:
1. Use LSTM. Extract the hidden layer from last block. Use this feature map as an input to fully connected layers and subsequently train it to make a prediction.
2. Use methods of Natural Language Processing.
  a. Remove stop words.
  b. Stemming
  c. TF-IDF
  d. Find frequently used words after a,b,c
  and many more.
 
Method 1, that is using LSTM will prove ineffective due to lack of data. It requires a lot of data to train LSTM and fully connected layers. So we decided to switch to method 2. 

## Step 2: Building a basic Categorization tool
We tried building a basic category predictor using Method 2 described above. We employed Multinomial Naive Bayes Classifier and NLP techniques on the text(2c and 2d). We temporarily used "fetch_20 news groups"_ available in sklearn library of python. You can find the code in [baseline.ipynb](https://github.com/Maitreyapatel/IngeniousHackathon_Tritons/blob/master/baseline.ipynb).

## Step 3: Build a small dataset manually
Presently, we do not have a dataset with text descriptions and CPV's of goods, so we decided to build a small dataset for trial runs.

Method of building dataset:
1. Choose 5 categories.
2. Choose a few sub-categories under each one.
3. Manually collect text descriptions of sub categories for all the main categories.
This resulted us in 12 descriptions per main category. In total we have, 60 instances(12*5) in our final dataset.

Categories we chose: Construction Work, Agriculture, Clothing, IT Services, Financial Services

## Step 4: Running our basic categorizer on new dataset
## Step 5: Stemming the input data
Stemming will enable us to extract useful statistics to analyze the input text. The goal of a stemmer is to reduce words in their different forms into a common base form. It is basically a heuristic process that cuts off the ends of words to extract their base forms. 
Result: The keywords does not include redundant words like 'and' , 'the', 'is', 'to' and so on. The top keywords are now more relevant to the reviews.

## Step 6: Linking the output categories to CPV codes


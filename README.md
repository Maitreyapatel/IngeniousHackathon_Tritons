# IngeniousHackathon_Tritons

##Aim: To build a category predictor. The input is in the form of text description. We need to classify the category which the text belongs.
The categories are CPV's of goods as formulated by European Union. This is helpful for categorising government tendors into different product categories. 


##Approach:
Given a description, we will first find the product which describes it. Then find the assigned CPV of that product.

The CPV consists of a main vocabulary and a supplementary vocabulary.

The main vocabulary is based on a tree structure comprising codes of up to nine digits associated with a wording that describes the supplies, works or services forming the subject of the contract.

    The first two digits identify the divisions (XX000000-Y);
    The first three digits identify the groups (XXX00000-Y);
    The first four digits identify the classes (XXXX0000-Y);
    The first five digits identify the categories (XXXXX000-Y);

Each of the last three digits gives a greater degree of precision within each category.

##Setting the Design Philosophy of a categoriser:
Find the probability of categories which the description belongs to. 
In order to classify on the basis of probability, we have two methods:
1. Use LSTM. Extract the hidden layer from last block. Use this feature map as an input to fully connected layers and subsequently train it to make a prediction.
2. Use methods of Natural Language Processing.
  a. Remove stop words.
  b. Stemming
  c. TF-IDF
  d. Find frequently used words  after a,b,c.
 We are deciding the other methods and parameters for categorisation.
 
 Method 1, that is using LSTM will prove ineffective due to lack of data. It requires a lot of data to train LSTM and fully connected layers. So we decided to switch to method 2.
 Currently, we do not have a dataset.
 In subsequent hours, we will be building a small dataset including 5-6 categories. 
 



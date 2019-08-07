# University_Recommendation_System


# Background & Objectives of Project:
For an aspiring student who wants to apply for higher studies in other countries, university selection process is a challenging task as lot of different criteria need to considered during application process based on individual’s requirement. This problem can be addressed by modeling a recommender system based on various classification algorithms. In this project based on the student dataset and user profile, a list of 10 best universities will be suggested such that it maximizes the chances of a student getting admission into those universities.

# DataSet:
The first step in building any recommendation system is the identification of the data set. So, the graduate student data was scraped from www.thegradcafe.com and the Undergraduate student data was scraped from https://collegescorecard.ed.gov/data/. About 271807 rows of raw student data was obtained as a result of web scraping, which is being processed to use as final dataset.

# Analysis & Methodology:
Here I have used Knowledge based recommendation System where User inputs are taken into account and compare with the training data.

For Graduate University Recommendation I have used Case based knowledge recommendation as it will take the User inputs and compare with trained data.
For Undergraduate Recommendation System, I have used Constraint based Knowledge recommendation system where user inputs taken into account as constraints and based on the constraints we will compare with trained data.

# Models:
I used two different models like K-Nearest Neighbors and Feature weighted algorithms.

# K Nearest Neighbor: 
In KNN, the trained data is compared with test data and distances are calculated using Euclidean distance. It then classifies an instance by finding its nearest neighbors and recommend the top n nearest neighbor universities. Algorithm is stated as below.

1. Initialize the value of k
2. For getting recommendation, iterate from 1 to number of trained data
1. Calculate distance between test data and each row
2. Sort the distances in ascending order
3. Get top k rows and recommend to the user

# Feature weighted algorithm: 
The weightage of all the features are taken and find the similarity score. Based on the similarity score, the universities with highest similarities will be recommended to student. Suppose w1, w2 are weights and f1 and f2 are features the similarity is calculated by formula
Similarity score = w1* f1+w2*(1-f2)

Setup:

1. Download the entire repository
2. go into the project folder and into  webscrape/csv folder , Unzip all the zipped files into csv folder(I have uploaded zipped files as the github is not accepting the files which are more than 50 MB) 
3. run npm install
4. cd server
5. python server.py
6. run the application in http://localhost:5000

If you want to check the web scraping code 
1. cd WebScraped_data 
2. Ipython notebook webscrape.ipynb

Web Application:

The Web aplication is created using python Flask and Bootstrap framework

Once the application is running, The home page will appear as below.

![Home Page](/images/home.png?raw=true "Optional Title")

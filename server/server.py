import random
from flask import Flask, render_template, escape, request, redirect
import pandas as pd
import numpy as np
import csv
import math
from sklearn import neighbors, datasets
from numpy.random import permutation
from sklearn.metrics import precision_recall_fscore_support
import UnderGraduateServer
app = Flask(__name__, static_folder='../static/dist', template_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graduate')
def graduate():
    return render_template('graduate.html')

@app.route("/main")
def return_main():
    return render_template('index.html')

@app.route('/undergraduate')
def undergraduate():
    return render_template('undergraduate.html')

def euclidean_dist(test, train, length):
    distance = 0
    for x in range(length):
        distance += np.square(test[x] - train[x])
    return np.sqrt(distance)


def knn(trainSet, test_instance, k):
 
    distances = {}
    sort = {}
    length = test_instance.shape[1]

    for x in range(len(trainSet)):
 
        distance = euclidean_dist(test_instance, trainSet.iloc[x], length)
        distances[x] = distance[0]

    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    print(sorted_distances[:5])

 
    neighbors_list = []

    for x in range(k):
        neighbors_list.append(sorted_distances[x][0])

    duplicateNeighbors = {}

    for x in range(len(neighbors_list)):
        responses = trainSet.iloc[neighbors_list[x]][-1]
        
        if responses in duplicateNeighbors:
            duplicateNeighbors[responses] += 1
        else:
            duplicateNeighbors[responses] = 1
    print(responses)

    sortedNeighbors = sorted(duplicateNeighbors.items(), key=lambda x: x[1], reverse=True)
    return(sortedNeighbors, neighbors_list)





@app.route('/undergraduatealgo')
def undergraduatealgo():
    result = UnderGraduateServer.main()
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    return '''
        <html>
            <head>
                <title>University Recommendation Application</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
            </head>
            <body>
                <div class="container">
                    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
                        <h3 class="navbar-brand">Undergraduate Recommendations</h3>
                        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample05" aria-controls="navbarsExample05" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarsExample05">
                            <ul class="navbar-nav mr-auto">
                                <li class="nav-item active">
                                    <a class="nav-link" href="/main">Home</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/undergraduate">Undergraduate College<span class="sr-only">(current)</span></a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/graduate">Graduate College</a>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>

                <div class="container">
                    <div class="jumbotron">
                        <h1>University Recommendation system</h1>
                        <p class="lead"></p>
                          <p>The top recommended Universities based on your SAT Score & Maximum Tution Fee are </p>
                            <table>
                            <tr><td><h4>S.No</h4></td><td><h4>University</h4></td><td><h4>Acceptance Rate</h4></td></tr>
                            <tr><td><p>1. </p></td><td>{result10}</td><td>{result11}</td></tr>
                            <tr><td><p>2. </p></td><td>{result20}</td><td>{result21}</td></tr>
                            <tr><td><p>3. </p></td><td>{result30}</td><td>{result31}</td></tr>
                            <tr><td><p>4. </p></td><td>{result40}</td><td>{result41}</td></tr>
                            <tr><td><p>5. </p></td><td>{result50}</td><td>{result51}</td></tr>
                            </table>
                    </div>
     

                    <footer class="footer">
                    </footer>
                </div>
            </body>
        </html>
            '''.format(result10 = list1[0], result11 = list2[0], result20 = list1[1], result21 = list2[1],result30 = list1[2],result31 = list2[2], result40 = list1[3], result41 = list2[3],result50 = list1[4], result51 = list2[4])

  
@app.route('/graduatealgo')
def graduatealgo():
    data = pd.read_csv('../WebScraped_data/csv/processed_data.csv')
    data.drop(data.columns[data.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    greV = float(request.args.get("greV"))
    greQ = float(request.args.get("greQ"))
    greA = float(request.args.get("greA")) 
    cgpa = float(request.args.get("cgpa"))
    testSet = [[greV, greQ, greA, cgpa]]
    test = pd.DataFrame(testSet)
    k = 7
    result,neigh = knn(data, test, k)
    list1 = []
    list2 = []
    for i in result:
        list1.append(i[0])
    for i in result:
        list2.append(i[1])
    for i in list1:
        print(i)
    return '''
        <html>
            <head>
                <title>University Recommendation Application</title>
                
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb" crossorigin="anonymous">
                <link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet">
            </head>
            <body>
                <div class="container">
                    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
                        <h3 class="navbar-brand">Graduate Recommendations</h3>
                        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample05" aria-controls="navbarsExample05" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarsExample05">
                            <ul class="navbar-nav mr-auto">
                                <li class="nav-item active">
                                    <a class="nav-link" href="/main">Home</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/undergraduate">Undergraduate College</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/graduate">Graduate College<span class="sr-only">(current)</span></a>
                                </li>
                            </ul>
                        </div>
                    </nav>
                </div>

                <div class="container">
                    <div class="jumbotron">
                        <h1>University Recommendation system</h1>
                        <p class="lead"></p>
                            <p>
                                The top recommended Universities based on GRE score and GPA are 
                            </p>
                            <table>
                            
                            <tr><td><h4>S.No</h4></td><td><h4>University</h4></td></tr>
                            <tr><td><p>1. </p></td><td>{result10}</td></tr>
                            <tr><td><p>2. </p></td><td>{result20}</td></tr>
                            <tr><td><p>3. </p></td><td>{result30}</td></tr>
                            <tr><td><p>4. </p></td><td>{result40}</td></tr>
                            <tr><td><p>5. </p></td><td>{result50}</td></tr>
                            </table>
                    </div>
     

                    <footer class="footer">
                    </footer>
                </div>
            </body>
        </html>
            '''.format(result10 = list1[0], result20 = list1[1],result30 = list1[2], result40 = list1[3],result50 = list1[4])



if __name__ == '__main__':
    app.run()

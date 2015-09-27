# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 23:14:17 2015

@author: wcramblit
"""

import pandas as pd
import sklearn.cross_validation as sklcv
import sklearn.ensemble as sklens
import itertools
import sklearn.metrics as sklmets

#import train column names
cols = pd.read_table('UCI HAR Dataset/features.txt',header=None, sep='\s*')
del cols[0]
#delete num row
#clean colnames
cleancols = map(lambda x: x.replace("(",""), cols[1])
cleancols = map(lambda x: x.replace(")",""), cleancols)
cleancols = map(lambda x: x.replace("-","_"), cleancols)
cleancols = map(lambda x: x.replace(",","_"), cleancols)
cleancols = map(lambda x: x.replace("mean","Mean"), cleancols)
cleancols = map(lambda x: x.replace("std","STD"), cleancols)

#import train data (x train) and set column names
df = pd.read_table('UCI HAR Dataset/train/x_train.txt', sep='\s*',engine='python',header=None, names=cleancols)

#import train data labels (y train)
train_y = pd.read_table('UCI HAR Dataset/train/y_train.txt', sep='\s*',engine='python',header=None)
df['activity_labels'] = train_y

#change data labels to categoricals
#build dict with k,v pairs

vals = {1:"WALKING",
       2: "WALKING_UPSTAIRS",
       3: "WALKING_DOWNSTAIRS",
       4: "SITTING",
       5: "STANDING",
       6: "LAYING"
       }

#apply to activity_labels column
df['activity_labels'] = df['activity_labels'].apply(lambda x: vals.get(x,x))


#split data into training, test and validation sets
train, test = sklcv.train_test_split(df, test_size=0.3,random_state=30)
test_y = test.loc[:,'activity_labels']
test_x = test
del test_x['activity_labels']
train_y = train.loc[:,'activity_labels']
train_x = train
del train_x['activity_labels']

#fit a random forest classifier with 500 estimators to the training set
forest = sklens.RandomForestClassifier(n_estimators=500,max_features=0.33)
model = forest.fit(train_x, train_y)

#rank features by their importance scores. what are the top 10 important features?
title = ['score'] #to pass title to imps
imps = pd.DataFrame(model.feature_importances_, columns=title) #importances calculated
names = pd.DataFrame(cleancols, columns=None) #grab field names
imps['field'] = names #create df with importances and fields

#sort df to find top and bottom
imps.sort('score',ascending=False,inplace=True,kind='quicksort')
#print ordered
print imps[:10]

#what is the 10th feature's importance score: 3%

'''

RESULTS:

        score                    field
52   0.077342        tGravityAcc_min_X
40   0.063003       tGravityAcc_Mean_X
41   0.044471       tGravityAcc_Mean_Y
558  0.039783       angleX_gravityMean
559  0.037690       angleY_gravityMean
50   0.036029        tGravityAcc_max_Y
56   0.033952     tGravityAcc_energy_X
508  0.031261       fBodyAccMag_energy
73   0.031132  tGravityAcc_arCoeff_Z_1
74   0.030284  tGravityAcc_arCoeff_Z_2



'''

# What is your model's mean accuracy score on the validation and test sets?

predictions = model.predict(test_x)
score_array = [i for i, j in zip(test_y, predictions) if i == j]
correct_preds = float(len(score_array))
total_preds = float(len(predictions))

calc_score = correct_preds/total_preds

# mean accuracy (calc_score) is 96%

#What is your model's precision and recall score on the test set?
# NOTE: error returned on use of .oob_score_ (no attribute)
score = model.score(test_x,test_y)
score

# Score is 96%
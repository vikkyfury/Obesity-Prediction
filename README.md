<center><h1>Obesity Prediction</h1></center>

It is a multiclass prediction task.

## Problem Statement
Develop a multi-class prediction model to assess obesity risk, focusing on its association with cardiovascular disease.

## Features
* id – Person Number
* Gender - Person gender
* Age – Age of the person
* Height – Height of the person
* Family_history_with_overweight – Is there any person in family with over
weight
* FAVC – Food and Vegetable Consumption
* FCVC – Fruit and Vegetable Consumption
* NCP – Nutritional Counseling Program
* CAEC – Childhood Adverse Experiences and Childhood Obesity
* SMOKE – Smoking
* CH2O – Water Consumption
* SCC – Sedentary Lifestyle and Central Obesity
* FAF – Frequency of Fast-Food Consumption
* TUE – Television Viewing and Obesity
* CALC – Caloric Intake
* MTRANS – Mode of Transportation
* NObeyesed – It tells whether the person is obese or not and its types. And type of obese.

## Output types
The predictions obtained in the results page will be one of them:

0: 'Insufficient Weight'

1: 'Normal Weight'

2: 'Overweight Level I'

3: 'Overweight Level II'

4: 'Obesity Type I'

5: 'Obesity Type II'

6: 'Obesity Type III'

## Models
We used Neural Netowrk model for deployement. We also used Logistic Regression, KNN, Naive Bayes, SVM models. 
After using different ml methods on the dataset ‘Multi-class Prediction of
Obesity Risk’. Based on the results we conclude that the neural
networks are comparatively performing better than other ml techniques.
So, we have considered the neural network model for developing the user
interface.

## User Interface
Created a basic UI so that from the given input data the model can predict the Obesity level.


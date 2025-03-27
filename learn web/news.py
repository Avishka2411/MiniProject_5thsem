import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import string
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
data_fake=pd.read_csv('Fake')
data_true=pd.read_csv('True')
data_fake["class"]=0
data_true['class']=1
data_fake_manual_testing = data_fake.tail(10)
# Get the last 10 valid indices of data_fake
last_valid_index_fake = data_fake.index[-1]
for i in range(last_valid_index_fake, last_valid_index_fake - 10, -1):
    data_fake.drop([i], axis=0, inplace=True)
data_true_manual_testing = data_true.tail(10)
# Get the last 10 valid indices of data_true
last_valid_index_true = data_true.index[-1]
for i in range(last_valid_index_true, last_valid_index_true - 10, -1):
    data_true.drop([i], axis=0, inplace=True)

data_fake_manual_testing['class']=0
data_true_manual_testing['class']=1
data_merge=pd.concat([data_fake, data_true], axis = 0)
#data_merge.columns
data=data_merge.drop(['title','subject','date'], axis = 1)
data = data.sample(frac = 1)
import string

def wordopt(text):
    # Check if the input is a string before applying string operations
    if isinstance(text, str):
        text = text.lower()
        text = re.sub('\[.*?\]','',text)
        text = re.sub("\\W"," ",text)
        text = re.sub('https?://\S+|www\.\S+','',text)
        text = re.sub('<.*?>+', '',text) # removed "b" flag
        text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
        text = re.sub('\w*\d\w*','',text)
        return text
    # If not a string, return the original value (or handle it as needed)
    else:
        return text

data['text'] = data['text'].fillna('')

x = data['text']
y = data['class']

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25)

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)
#Linear Regression
from sklearn.linear_model import LogisticRegression
LR = LogisticRegression()
LR.fit(xv_train, y_train)
pred_lr = LR.predict(xv_test)

#DecisionTreeClassifier
from sklearn.tree import DecisionTreeClassifier

DT = DecisionTreeClassifier()
DT.fit(xv_train, y_train)
pred_dt = DT.predict(xv_test)

#GradientBoostingClassifier
from sklearn.ensemble import GradientBoostingClassifier

GB = GradientBoostingClassifier(random_state = 0)
GB.fit(xv_train, y_train)
pred_gb = GB.predict(xv_test)

#RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(random_state = 0)
RF.fit(xv_train, y_train)
pred_rf = RF.predict(xv_test)

def output_lable(n):
    if n==0:
        return "Fake News"
    elif n==1:
        return "Not A Fake News"

def manual_testing(news):
    testing_news = {"text":[news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test['text'] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    
    pred_RF = RF.predict(new_xv_test)
    return str("\n\nLR Predicition: {} \nDT Prediction: {} \nRFC Prediction:{}".format(output_lable(pred_LR[0]),
                                                                                                            output_lable(pred_DT[0]),
                                                                                                            
                                                                                                            output_lable(pred_RF[0])))

st.title("Fake News Detection")
st.image("Fake-News-Detection.jpg.webp")
st.subheader("Write news here")
user_input= st.text_input(" ")
submit= st.button("check")
if submit:
    answer= manual_testing(user_input)
    st.text(answer)

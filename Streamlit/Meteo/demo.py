import streamlit as st 
st.title("Titre")
st.header("Sous titre")
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

models = ["Random Forest Classifier","Logistic Regression","SVM"]
x =st.selectbox("Ceci est une selectbox",["A","B","C"])
model_name =st.selectbox("Ceci est un modele",models )

if model_name ==models[0]:
    model = RandomForestClassifier()
if model_name ==models[1]:
    model = LogisticRegression()
if model_name ==models[2]:
    model = SVC()

st.write(x)

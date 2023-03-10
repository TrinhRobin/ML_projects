import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
df =pd.read_csv("test.csv")
X_train, X_test, y_train, y_test = train_test_split(df[["height(cm)","length(m)","X1","X2"]],df["color_type"])
def score(option_choice):
    if option_choice== "KNN":
        model = KNeighborsClassifier()
    if option_choice== "Logit":
        model = LogisticRegression()
    if option_choice== "Random Forest":
        model = RandomForestClassifier()
    model.fit(X_train,y_train)
    return(model.score(X_test,y_test))

def predict(option_choice,user_input):
    if option_choice== "KNN":
        model = KNeighborsClassifier()
    if option_choice== "Logit":
        model = LogisticRegression()
    if option_choice== "Random Forest":
        model = RandomForestClassifier()
    model.fit(X_train,y_train)
    return(model.predict(user_input))
    

page = st.sidebar.radio("Choose a page",
options= ["Presentation","Data viz","Modelisation"])
if page == "Presentation":
    st.title("This  a Demo of Streamlit")
    st.header("By the Datascientest Team")
    st.write("My project about multiple target variable classification")
    st.image("dataset-cover.jpeg")
    st.dataframe(df.head())
    st.markdown("This is the [link](https://www.kaggle.com/datasets/ppsheth91/two-target-variables-classification-problem) to the original dataset")
    st.write("And a cool video about this topic")
    st.video("https://www.youtube.com/watch?v=rZwq7J2QETw",start_time=35)
if page == "Data viz":
    fig, ax = plt.subplots()
    sns.barplot(y="color_type", x="length(m)",data=df,orient='h')

    ax.set_yticks([i for i in range(len(df['color_type'].unique())) if i%2==0])
    # Set ticks labels for y-axis
    ax.set_yticklabels([df['color_type'].unique()[i] for i in range(len(df['color_type'].unique())) if i%2==0] , rotation='horizontal', fontsize=12)
    st.pyplot(fig,legend =" A visualisation about the dataframe")

    fig2, ax2 = plt.subplots()
    sns.boxplot(x="color_type", y="height(cm)",data=df)

    ax2.set_xticks([i for i in range(len(df['color_type'].unique())) if i%2==0])
    # Set ticks labels for x-axis
    ax2.set_xticklabels([df['color_type'].unique()[i] for i in range(len(df['color_type'].unique())) if i%2==0] , rotation='vertical', fontsize=12)
    st.pyplot(fig2,legend =" A Second visualisation about the dataframe")
    
    fig3 = plt.figure()
    sns.scatterplot(x='X1',y='X2',data=df)
    st.pyplot(fig3,legend =" A third visualisation about the dataframe")

if page == "Modelisation":
    st.markdown("This is our ML model")
    models = ["KNN","Logit","Random Forest"]
    model_name =st.selectbox("Choose a Classification Model",models)
    st.write("The performance is :",score(model_name))

    st.write("Maybe we can do some predictions ?")

    number1 = st.slider('Insert a number for height(cm)?', df['height(cm)'].min(),df['height(cm)'].max(), 1.)
    number2 = st.slider('Insert a number for  length(m)?', df['length(m)'].min(),df['length(m)'].max(), 0.01)

    number3 = st.number_input('Insert a number for "X1"')
    number4 = st.number_input('Insert a number for "X2":')
    st.write(f"The result of the ML Model is : {predict(model_name,pd.DataFrame({ 'height(cm)':number1, 'length(m)' :number2,  'X1':number3, 'X2':number4},index=[1]))}")
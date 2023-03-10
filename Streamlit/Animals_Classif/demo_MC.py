import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df= pd.read_csv("test.csv")
X_train,X_test,y_train, y_test = train_test_split(df[["length(m)","height(cm)","X1","X2"]],df['color_type'])

options=["KNN","Logistic Regression","Random Forest"]
def get_score(model_name):
    if model_name==options[0]:
        model = KNeighborsClassifier()
    if model_name==options[1]:
        model = LogisticRegression()
    if model_name==options[2]:
        model = RandomForestClassifier()
    model.fit(X_train,y_train)
    return(model.score(X_test,y_test))

def get_predictions(model_name,user_inputs):
    if model_name==options[0]:
        model = KNeighborsClassifier()
    if model_name==options[1]:
        model = LogisticRegression()
    if model_name==options[2]:
        model = RandomForestClassifier()
    model.fit(X_train,y_train)
    return(model.predict(user_inputs))

page = st.sidebar.radio("Choose a page", options=["Presentation","Visualization","Modeling"])
if page == "Presentation":
    st.title('An introduction on streamlit')
    st.header("By Datascientest")
    st.dataframe(df.head())
    st.image("dataset-cover.jpeg",caption="A cool picture about the dataset")
    st.write("The columns' names are",df.columns)
    st.markdown("This is the [link](https://www.kaggle.com/datasets/ppsheth91/two-target-variables-classification-problem) towards the original dataset")
if page == "Visualization":
    fig,ax = plt.subplots()
    sns.barplot(data = df, y= "color_type",x= "length(m)",orient='h')
    ax.set_yticks([i for i in range(len(df["color_type"].unique()) )if i%2==0 ],rotation='vertical',fontsize=12)
    st.pyplot(fig)

    fig,ax = plt.subplots()
    sns.boxplot(data = df, y= "color_type",x= "height(cm)",orient='h')
    ax.set_yticks([i for i in range(len(df["color_type"].unique()) )if i%2==0 ],rotation='vertical',fontsize=12)
    st.pyplot(fig)
    

    fig3 = plt.figure()
    sns.scatterplot(data=df,x='X1',y='X2')
    st.pyplot(fig3)
if page == "Modeling":
    model_name =st.selectbox("Choose a ML Model to train",options=["KNN","Logistic Regression","Random Forest"])
    st.write(f"The performance of the ML model is {get_score(model_name)}")

    var1 = st.slider("Choose the value for length(m)",df["length(m)"].min(),df["length(m)"].max(), 0.1)
    var2 = st.slider("Choose the value for height(cm)",df["height(cm)"].min(),df["height(cm)"].max(), 1.)
    var3 = st.number_input(" Choose the value for X1 :" )
    var4 = st.number_input(" Choose the value for X2 :" )
    inputs = pd.DataFrame({'length(m)': var1, 'height(cm)' :var2,
                    'X1': var3,'X2':var4},index=[1])
    st.write(f'The prediction of the ML model is ',get_predictions(model_name,inputs))
    st.write( ' "Cogito ergo sum" Descartes')
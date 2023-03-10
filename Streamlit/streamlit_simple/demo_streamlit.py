import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
df =pd.read_csv("transactions.csv",index_col=0)


X_train, X_test, y_train, y_test = train_test_split(df[["ProductUnitPrice","ClientZipCode"]],df["ProductDiscount"])
def score(option_choice):
    if option_choice== "KNN":
        model = KNeighborsClassifier()
    if option_choice== "Logit":
        model = LogisticRegression()
    if option_choice== "Random Forest":
        model = RandomForestClassifier()
    model.fit(X_train,y_train)
    return(model.score(X_test,y_test))




page = st.sidebar.radio("Choose a page",
options= ["Presentation","Data viz","Modelisation"])

if page == "Presentation":
    st.title("This  a Demo of Streamlit")
    st.header("By the Datascientest Team")
    st.write(" Some text")
    st.image("Robin.png")
    st.dataframe(df.head())
    st.markdown("This is the [link](https://formation.datascientest.com/nos-formations?utm_term=datascientest&utm_campaign=%5Bsearch%5D+data+analyst&utm_source=adwords&utm_medium=ppc&hsa_acc=9618047041&hsa_cam=14490023985&hsa_grp=126147897829&hsa_ad=542987827577&hsa_src=g&hsa_tgt=kwd-810260702289&hsa_kw=datascientest&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gclid=CjwKCAiAs8acBhA1EiwAgRFdw4C11x9Sqbn09xSNBb242AV9Il2WvtBMxjGqoQqhGakk4E5QbOvMlxoCggEQAvD_BwE) to the webstote")
if page == "Data viz":
    fig = plt.figure()
    sns.countplot(x="ProductDiscount",data=df)
    st.pyplot(fig,legend =" A visualisation about the dataframe")
if page == "Modelisation":
    st.markdown("This is our ML model")
    models = ["KNN","Logit","Random Forest"]
    model_name =st.selectbox("Choose a Classification Model",models)
    st.write("The performance is :",score(model_name))